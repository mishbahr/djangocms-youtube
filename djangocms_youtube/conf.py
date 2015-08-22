# -*- coding: utf-8 -*-

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class DjangoCMSYoutubeConf(AppConf):
    PLUGIN_MODULE = _('Generic')
    PLUGIN_NAME = _('Youtube')

    FIELDSETS = None
    PAGE_ONLY = False
    PARENT_CLASSES = None
    REQUIRE_PARENT = False
    TEXT_ENABLED = False
    ALLOW_CHILDREN = True
    CHILD_CLASSES = None
    USE_HTTPS = False
    API_KEY = None

    ENABLE_CUSTOM_VIDEO_SIZE = False

    TEMPLATES = (
        ('djangocms_youtube/default.html', _('Default')),
    )

    DESCRIPTION_CHOICES = (
        ('hidden', _('Do Not Display Description')),
        ('below', _('Description Below the Video')),
    )

    DEFAULT_HEIGHT = 480
    DEFAULT_WIDTH = 854

    DEFAULT_THEME = 'light'
    THEME_CHOICES = (
        ('dark', _('Dark')),
        ('light', _('Light')),
    )

    THUMBNAIL_SIZES = {
        'default': {
            'width': 120,
            'height': 90
        },
        'high': {
            'width': 480,
            'height': 360
        },
        'medium': {
            'width': 320,
            'height': 180
        },
        'maxres': {
            'width': 1280,
            'height': 720
        },
        'standard': {
            'width': 640,
            'height': 480
        }
    }

    class Meta:
        prefix = 'djangocms_youtube'
