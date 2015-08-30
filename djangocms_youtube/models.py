# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.sites.models import Site
from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from isodate import parse_datetime, parse_duration
from jsonfield import JSONField

from .conf import settings

logger = logging.getLogger('djangocms_youtube')


@python_2_unicode_compatible
class Youtube(CMSPlugin):
    title = models.CharField(_('Title'), max_length=150, blank=True)
    thumbnail = FilerImageField(
        verbose_name=_('Custom Thumbnail'), blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='djangocms_youtube_thumbnails',
        help_text=_('Image Overlay - this image will display over the '
                    'video on your site and allow users to see an image '
                    'of your choice before playing the video.'))
    video_url = models.URLField(
        _('Video URL'), help_text=_('Paste the URL of the YouTube video'))

    width = models.PositiveIntegerField(
        _('Width'), blank=True, null=True,
        help_text=_('Sets the width of your player, '
                    'used on some templates where applicable'))
    height = models.PositiveIntegerField(
        _('Height'), blank=True, null=True,
        help_text=_('Sets the height of your player, '
                    'used on some templates where applicable'))

    description = models.TextField(
        _('Video Description'), blank=True, null=True,
        help_text=_('You can add a Description to your video, to be '
                    'displayed beneath your video on your page.'))

    description_option = models.CharField(
        _('Description Option'), max_length=50,
        choices=settings.DJANGOCMS_YOUTUBE_DESCRIPTION_CHOICES,
        default=settings.DJANGOCMS_YOUTUBE_DESCRIPTION_CHOICES[0][0], blank=True)

    theme = models.CharField(
        _('Theme'), max_length=100,
        choices=settings.DJANGOCMS_YOUTUBE_THEME_CHOICES,
        default=settings.DJANGOCMS_YOUTUBE_DEFAULT_THEME,
    )
    plugin_template = models.CharField(
        _('Template'), max_length=255,
        choices=settings.DJANGOCMS_YOUTUBE_TEMPLATES,
        default=settings.DJANGOCMS_YOUTUBE_TEMPLATES[0][0],
    )

    video_data = JSONField(
        verbose_name=_('YouTube Data'), blank=True, null=True,
        help_text=_('For advanced users only — please do not edit '
                    'this data unless you know what you are doing.')
    )

    def __str__(self):
        return self.title

    @property
    def video(self):
        cls = Video(**self.video_data)
        return cls

    def _generate_thumbnails(self):
        _thumbnails = {}
        for name, opts in six.iteritems(settings.DJANGOCMS_YOUTUBE_THUMBNAIL_SIZES):
            try:
                thumb_opts = {
                    'size': (int(opts['width']), int(opts['height'])),
                    'subject_location': self.thumbnail.subject_location,
                    'crop': False,
                    'upscale': True,
                }
                thumb = self.thumbnail.file.get_thumbnail(thumb_opts)
                _thumbnails[name] = {
                    'url': thumb.url,
                    'width': opts['width'],
                    'height': opts['height']
                }
            except Exception as e:
                logger.error('Error while generating thumbnail: %s', e)
        return _thumbnails

    @property
    def highest_resolution_thumbnail(self):
        thumbnails = self.get_thumbnails()
        for size in ('maxres', 'standard', 'high', 'medium', 'default',):
            if size in thumbnails:
                return thumbnails[size]

    def get_thumbnails(self):
        if self.thumbnail_id is None:
            return self.video.get_thumbnails()

        return self._generate_thumbnails()

    def get_title(self):
        if self.title:
            return self.title
        return self.video.get_title()

    def get_description(self):
        return self.description

    def get_thumbnail(self):
        thumbnail = self.highest_resolution_thumbnail.get('url', '')
        protocol = 'https' if settings.DJANGOCMS_YOUTUBE_USE_HTTPS else 'http'
        if thumbnail.startswith('http'):
            return thumbnail

        current_site = Site.objects.get_current()
        return '{protocol}://{domain}{thumbnail}'.format(
            protocol=protocol,
            domain=current_site.domain,
            thumbnail=thumbnail
        )


@python_2_unicode_compatible
class Video(object):

    def __init__(self, *args, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def get_id(self):
        return getattr(self, 'id')

    def get_title(self):
        return self.snippet.get('title')

    def get_description(self):
        return self.snippet.get('description')

    def get_channel_title(self):
        return self.snippet.get('channelTitle')

    def get_embed_html(self):
        return self.player.get('embedHtml')

    def get_embed_url(self):
        return 'https://www.youtube.com/embed/{video_id}'.format(video_id=self.get_id())

    def get_thumbnails(self):
        return self.snippet.get('thumbnails', {})

    def get_duration(self):
        return self.contentDetails.get('duration')

    def get_duration_seconds(self):
        duration = parse_duration(self.get_duration())
        return duration.total_seconds()

    def get_published_at(self):
        return self.snippet.get('publishedAt')

    def get_published_datetime(self):
        return parse_datetime(self.get_published_at())

    def get_tags(self):
        return self.snippet.get('tags', [])

    def __str__(self):
        return 'Video: %s' % self.id
