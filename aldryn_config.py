# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aldryn_client import forms


class Form(forms.BaseForm):
    plugin_module = forms.CharField('Plugin module name', initial='Generic')
    plugin_name = forms.CharField('Plugin name', initial='Youtube')
    use_https = forms.CheckboxField(
        'Use HTTPS?', initial=False, required=False,
        help_text='Check this box to use HTTPS for thumbnail URLS')
    api_key = forms.CharField(
        'YouTube Data API key',
        help_text='You can register an app via '
                  'https://developers.google.com/youtube/registering_an_application')

    def to_settings(self, data, settings):
        settings['DJANGOCMS_YOUTUBE_PLUGIN_MODULE'] = data['plugin_module']
        settings['DJANGOCMS_YOUTUBE_PLUGIN_NAME'] = data['plugin_name']
        settings['DJANGOCMS_YOUTUBE_USE_HTTPS'] = data['use_https']
        settings['DJANGOCMS_YOUTUBE_API_KEY'] = data['api_key']
        return settings
