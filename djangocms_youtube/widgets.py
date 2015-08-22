# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse

from .models import Youtube


class YoutubeVideoURLWidget(forms.TextInput):
    model = Youtube

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        opts = self.model._meta

        app_label = opts.app_label
        try:
            model_name = opts.model_name
        except AttributeError:
            model_name = opts.module_name

        attrs['data-gdata'] = reverse('admin:%s_%s_%s' % (app_label, model_name, 'gdata',))
        return super(YoutubeVideoURLWidget, self).render(name, value, attrs)
