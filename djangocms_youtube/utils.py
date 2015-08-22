# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from requests.api import request
from requests.exceptions import RequestException

from .conf import settings
from .exceptions import YoutubeAPIError


def get_video_details(video_id):
    access_token = settings.DJANGOCMS_YOUTUBE_API_KEY
    if access_token is None:
        msg = _('Missing DJANGOCMS_YOUTUBE_API_KEY settings')
        raise YoutubeAPIError(500, 'ImproperlyConfigured', force_text(msg))

    yt_endpoint = \
        'https://www.googleapis.com/youtube/v3/videos' \
        '?part=snippet,player,status,contentDetails&id={0}&key={1}'.format(
            video_id, access_token)

    try:
        response = request('get', url=yt_endpoint)
        response.raise_for_status()
    except RequestException as e:
        error = e.response.json().get('error')
        raise YoutubeAPIError(error['code'], 'YoutubeAPIError', error['message'])
    else:
        results = response.json().get('items', [])
        if not results:
            msg = _('This video does not exist.')
            raise YoutubeAPIError(404, 'videoNotFound', force_text(msg))
        else:
            return results[0]
