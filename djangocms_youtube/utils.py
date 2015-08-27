# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from requests.api import request
from requests.exceptions import RequestException

from .conf import settings
from .exceptions import YoutubeAPI404, YoutubeAPIError


def fetch_gdata(resource, parts, identifier):
    access_token = settings.DJANGOCMS_YOUTUBE_API_KEY

    if access_token is None:
        msg = _('Missing DJANGOCMS_YOUTUBE_API_KEY settings')
        raise YoutubeAPIError(500, 'ImproperlyConfigured', force_text(msg))

    url_template = '{resource}?part={parts}&fields=items&maxResults=1&id={id}&key={access_token}'
    url = url_template.format(
        resource=resource,
        parts=','.join(parts),
        id=identifier,
        access_token=access_token,
    )

    base_url = 'https://www.googleapis.com/youtube/v3/'
    try:
        response = request('get', url='{base_url}{url}'.format(base_url=base_url, url=url))
        response.raise_for_status()
    except RequestException as e:
        error = e.response.json().get('error')
        raise YoutubeAPIError(error['code'], 'YoutubeAPIError', error['message'])
    else:
        items = response.json().get('items', [])
        if not items:
            raise YoutubeAPI404()
        return items[0]


def get_video_details(video_id):
    parts = ('snippet', 'player', 'status', 'contentDetails', )
    try:
        result = fetch_gdata('videos', parts, video_id)
    except YoutubeAPI404:
        msg = _('This video does not exist.')
        raise YoutubeAPIError(404, 'videoNotFound', force_text(msg))
    else:
        category_name = get_category_name(result.get('snippet', {}).get('categoryId', ''))
        result['snippet']['categoryName'] = category_name
        return result


def get_category_name(cat_id):
    parts = ('snippet', )
    try:
        result = fetch_gdata('videoCategories', parts, cat_id)
    except YoutubeAPI404:
        msg = _('This video category does not exist.')
        raise YoutubeAPIError(404, 'videoCategoryNotFound', force_text(msg))
    else:
        return result.get('snippet', {}).get('title', '')
