# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.http import HttpResponseNotAllowed
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .exceptions import YoutubeAPIError
from .forms import YoutubeModelForm
from .models import Youtube
from .utils import get_video_details

try:
    from django.http import JsonResponse
except ImportError:
    from .compat import JsonResponse


class YoutubePlugin(CMSPluginBase):
    model = Youtube
    form = YoutubeModelForm

    module = settings.DJANGOCMS_YOUTUBE_PLUGIN_MODULE
    name = settings.DJANGOCMS_YOUTUBE_PLUGIN_NAME
    render_template = settings.DJANGOCMS_YOUTUBE_TEMPLATES[0][0]

    text_enabled = settings.DJANGOCMS_YOUTUBE_TEXT_ENABLED
    page_only = settings.DJANGOCMS_YOUTUBE_PAGE_ONLY
    require_parent = settings.DJANGOCMS_YOUTUBE_REQUIRE_PARENT
    parent_classes = settings.DJANGOCMS_YOUTUBE_PARENT_CLASSES
    allow_children = settings.DJANGOCMS_YOUTUBE_ALLOW_CHILDREN
    child_classes = settings.DJANGOCMS_YOUTUBE_CHILD_CLASSES

    def get_fieldsets(self, request, obj=None):
        if settings.DJANGOCMS_YOUTUBE_FIELDSETS:
            return settings.DJANGOCMS_YOUTUBE_FIELDSETS

        advanced_option_fields = ('theme', )
        if settings.DJANGOCMS_YOUTUBE_ENABLE_CUSTOM_VIDEO_SIZE:
            advanced_option_fields += ('width', 'height', )

        if len(settings.DJANGOCMS_YOUTUBE_TEMPLATES) > 1:
            advanced_option_fields += ('plugin_template', )

        fieldsets = (
            (None, {
                'fields': ('video_url', )
            }),
            (None, {
                'fields': ('thumbnail',)
            }),
            (None, {
                'fields': ('title', 'description', 'description_option', )
            }),
            (None, {
                'fields': advanced_option_fields
            }),
            (_('Video Meta'), {
                'classes': ('advanced', 'collapse'),
                'fields': ('video_data', ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        # returns the first template that exists, falling back to bundled template
        return select_template([
            instance.plugin_template,
            settings.DJANGOCMS_YOUTUBE_TEMPLATES[0][0],
            'djangocms_youtube/default.html'
        ])

    def get_model_info(self):
        # module_name is renamed to model_name in Django 1.8
        app_label = self.model._meta.app_label
        try:
            return app_label, self.model._meta.model_name
        except AttributeError:
            return app_label, self.model._meta.module_name

    def get_plugin_urls(self):
        from django.conf.urls import patterns, url
        info = self.get_model_info()

        return patterns(
            '',
            url(r'^gdata/$',
                admin.site.admin_view(self.youtube_data_api),
                name='%s_%s_gdata' % info),
        )

    def youtube_data_api(self, request):
        if not request.method == 'POST':
            return HttpResponseNotAllowed(['POST', ])

        video_id = request.POST.get('video_id', None)
        if video_id is None:
            response = {
                'status': 400,
                'error_type': 'idRequired',
                'error_message': '',
            }
            return JsonResponse(response, status=400)

        try:
            response = get_video_details(video_id)
        except YoutubeAPIError as e:
            response = {
                'status': e.status_code,
                'error_type': e.error_type,
                'error_message': e.error_message,
            }
            return JsonResponse(response, status=e.status_code)
        else:
            return JsonResponse(response)

    class Media:
        css = {
            'all': (
                'admin/css/djangocms_youtube/changeform.css',
            )
        }
        js = ('admin/js/djangocms_youtube/changeform.js', )

plugin_pool.register_plugin(YoutubePlugin)
