# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

from filer.fields.image import FilerImageField
from jsonfield import JSONField

from djangocms_youtube.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__latest__'),
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=150, verbose_name='Title', blank=True)),
                ('video_url', models.URLField(help_text='Paste the URL of the YouTube video', verbose_name='Video URL')),
                ('width', models.PositiveIntegerField(help_text='Sets the width of your player, used on some templates where applicable', null=True, verbose_name='Width', blank=True)),
                ('height', models.PositiveIntegerField(help_text='Sets the height of your player, used on some templates where applicable', null=True, verbose_name='Height', blank=True)),
                ('description', models.TextField(help_text='You can add a Description to your video, to be displayed beneath your video on your page.', null=True, verbose_name='Video Description', blank=True)),
                ('description_option', models.CharField(default=settings.DJANGOCMS_YOUTUBE_DESCRIPTION_CHOICES[0][0], max_length=50, verbose_name='Description Option', blank=True, choices=settings.DJANGOCMS_YOUTUBE_DESCRIPTION_CHOICES)),
                ('theme', models.CharField(default=settings.DJANGOCMS_YOUTUBE_DEFAULT_THEME, max_length=100, verbose_name='Theme', choices=settings.DJANGOCMS_YOUTUBE_THEME_CHOICES)),
                ('plugin_template', models.CharField(default=settings.DJANGOCMS_YOUTUBE_TEMPLATES[0][0], max_length=255, verbose_name='Template', choices=settings.DJANGOCMS_YOUTUBE_TEMPLATES)),
                ('video_data', JSONField(help_text='For advanced users only \u2014 please do not edit this data unless you know what you are doing.', null=True, verbose_name='YouTube Data', blank=True)),
                ('thumbnail', FilerImageField(related_name='djangocms_youtube_thumbnails', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='filer.Image', help_text='Image Overlay - this image will display over the video on your site and allow users to see an image of your choice before playing the video.', null=True, verbose_name='Custom Thumbnail')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
