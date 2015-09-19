# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.utils import translation

from cms.models import Title
from cms.models.fields import PlaceholderField

from .models import Youtube


class VideoElement(object):
    def __init__(self, plugin):
        self.plugin = plugin

    def get_thumbnail(self):
        return self.plugin.get_thumbnail()

    def get_title(self):
        return self.plugin.get_title()

    def get_description(self):
        return self.plugin.get_description()

    def get_embed_url(self):
        return self.plugin.video.get_embed_url()

    def get_duration(self):
        return int(self.plugin.video.get_duration_seconds())

    def get_publication_date(self):
        return self.plugin.video.get_published_at()

    def get_tags(self):
        return self.plugin.video.get_tags()


class VideoSitemap(object):
    model = None

    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop('language', None)
        super(VideoSitemap, self).__init__(*args, **kwargs)

    def get_language(self):
        return self.language or translation.get_language()

    def _get_youtube_plugins(self, obj):
        youtube_plugins = []
        for field in self.model._meta.fields:
            if isinstance(field, PlaceholderField):
                placeholder = getattr(obj, field.name, None)
                plugins = Youtube.objects.filter(
                    placeholder=placeholder, language=self.get_language())
                youtube_plugins.extend(plugins)
        return youtube_plugins

    def get_queryset(self):
        if self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                '{cls} is missing a QuerySet. '
                'Define {cls}.model or override {cls}.get_queryset()'.format(
                    cls=self.__class__.__name__)
            )
        return queryset

    def location(self, item):
        item.get_absolute_url()

    def get_urls(self):
        urls = []
        for obj in self.get_queryset():
            youtube_plugins = self._get_youtube_plugins(obj)
            if youtube_plugins:
                urls.append({
                    'location': self.location(obj),
                    'youtube_plugins': youtube_plugins,
                })
        return urls


class CMSVideoSitemap(VideoSitemap):
    model = Title

    def get_queryset(self):
        queryset = self.model._default_manager.public().filter(
            Q(redirect='') | Q(redirect__isnull=True),
            page__login_required=False,
            page__site=Site.objects.get_current(),
        ).order_by('page__path')
        return queryset

    def location(self, title):
        translation.activate(title.language)
        url = title.page.get_absolute_url(title.language)
        translation.deactivate()
        return url

    def get_urls(self):
        urls = []
        for title in self.get_queryset():
            youtube_plugins = Youtube.objects.filter(
                placeholder__page=title.page, language=title.language)
            if youtube_plugins.exists():
                urls.append({
                    'location': self.location(title),
                    'youtube_plugins': youtube_plugins,
                })
        return urls
