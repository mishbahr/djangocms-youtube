=============================
djangocms-youtube
=============================

.. image:: http://img.shields.io/travis/mishbahr/djangocms-youtube.svg?style=flat-square
    :target: https://travis-ci.org/mishbahr/djangocms-youtube/

.. image:: http://img.shields.io/pypi/v/djangocms-youtube.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-youtube/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/djangocms-youtube.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-youtube/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/djangocms-youtube.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-youtube/
    :alt: License

.. image:: http://img.shields.io/coveralls/mishbahr/djangocms-youtube.svg?style=flat-square
  :target: https://coveralls.io/r/mishbahr/djangocms-youtube?branch=master

YouTube embed plugin for your django-cms powered site with options for custom video thumbnails, analytics, SEO and more.

Quickstart
----------

1. Install ``djangocms-youtube``::

    pip install djangocms-youtube

2. Add ``djangocms_youtube`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'djangocms_youtube',
        ...
    )

3. Sync database (requires ``south>=1.0.1`` if you are using Django 1.6.x)::

    python manage.py migrate


4. Plugin requires Server API key to be able to use the YouTube Data API::

    DJANGOCMS_YOUTUBE_API_KEY = '<youtube_data_api_server_key>'

You can register an app via https://developers.google.com/youtube/registering_an_application

Features
--------
Reduce Page Load Time
=====================

When you embed any YouTube video on your website using standard IFRAME tags, you’ll be surprised to know how much extra weight that YouTube video will add to your page. The resources (CSS, images and JavaScript) will download even if the visitor on your website has chosen not to watch the embedded YouTube video.


.. image:: http://mishbahr.github.io/assets/djangocms-youtube/thumbnail/djangocms-youtube-004.png
  :target: http://mishbahr.github.io/assets/djangocms-youtube/djangocms-youtube-004.png
  :width: 768px
  :align: center

djangocms-youtube uses a clever workaround to reduce the time it takes to initially load the YouTube video player. Instead of embedding the full Youtube video player, it displays just the thumbnail images of the video and a “play” icon is placed over the video so that it looks like a video player.

.. image:: http://mishbahr.github.io/assets/djangocms-youtube/thumbnail/djangocms-youtube-001.png
  :target: http://mishbahr.github.io/assets/djangocms-youtube/djangocms-youtube-001.png
  :width: 768px
  :align: center

When the user hits the play button, the video thumbnail is replaced with the standard YouTube video player. The extra resources are thus loaded only when the user has decided to play the embedded video and not otherwise.

Note: Mobile devices require two taps to play the video. Tap the image once to remove it and display the video player. Then, tap the play button to begin the video.

High Resolution Thumbnail
=========================

Fetches the highest resolution thumbnail available from YouTube for a given video with options for custom video thumbnails using ``django-filer``.

.. code-block::

    {
      "default": {
        "url": "https://i.ytimg.com/vi/9bZkp7q19f0/default.jpg",
        "width": 120,
        "height": 90
      },
      "high": {
        "url": "https://i.ytimg.com/vi/9bZkp7q19f0/hqdefault.jpg",
        "width": 480,
        "height": 360
      },
      "medium": {
        "url": "https://i.ytimg.com/vi/9bZkp7q19f0/mqdefault.jpg",
        "width": 320,
        "height": 180
      },
      "maxres": {
        "url": "https://i.ytimg.com/vi/9bZkp7q19f0/maxresdefault.jpg",
        "width": 1280,
        "height": 720
      },
      "standard": {
        "url": "https://i.ytimg.com/vi/9bZkp7q19f0/sddefault.jpg",
        "width": 640,
        "height": 480
      }
    }


Schema.org Integration
======================

Full support for schema.org ``videoObject`` markup.

.. code-block::

  <div class="video-wrapper" itemprop="video" itemscope="" itemtype="http://schema.org/VideoObject">
      <meta itemprop="name" content="PSY - GANGNAM STYLE (강남스타일) M/V">
      <meta itemprop="duration" content="PT4M13S">
      <meta itemprop="thumbnailUrl" content="https://i.ytimg.com/vi/9bZkp7q19f0/maxresdefault.jpg">
      <meta itemprop="embedURL" content="https://www.youtube.com/embed/9bZkp7q19f0">
      <meta itemprop="uploadDate" content="2012-07-15T07:46:32.000Z">
      <meta itemprop="height" content="480">
      <meta itemprop="width" content="853">
      <meta itemprop="description" content="...">
  </div>

See https://developers.google.com/webmasters/videosearch/schema


Video Endscreen
===============

.. image:: http://mishbahr.github.io/assets/djangocms-youtube/thumbnail/djangocms-youtube-002.png
  :target: http://mishbahr.github.io/assets/djangocms-youtube/djangocms-youtube-002.png
  :width: 768px
  :align: center

Plugin can have child plugins (i.e  other plugins placed inside this plugin), rendered as an overlay, when the video finishes. You can disable this functionality by overriding ``DJANGOCMS_YOUTUBE_ALLOW_CHILDREN`` in your ``settings.py`` file

Google Analytics
================

.. image:: http://mishbahr.github.io/assets/djangocms-youtube/thumbnail/djangocms-youtube-003.png
  :target: http://mishbahr.github.io/assets/djangocms-youtube/djangocms-youtube-003.png
  :width: 768px
  :align: center

Automatically publishes the metrics listed below to your Google Analytics account.

.. code-block::

    + Play
    + 10% watched
    + 25% watched
    + 50% watched
    + 75% watched
    + 90% watched
    + Watch to end

Make sure you have installed the Google Analytics tracking scripts.

See https://developers.google.com/analytics/devguides/collection/analyticsjs/


Video Sitemap
=============

Generate a sitemap for your YouTube videos.

.. image:: http://mishbahr.github.io/assets/djangocms-youtube/thumbnail/djangocms-youtube-005.png
  :target: http://mishbahr.github.io/assets/djangocms-youtube/djangocms-youtube-005.png
  :width: 768px
  :align: center

**Video Sitemap Configuration**

Import ``CMSVideoSitemap`` from ``djangocms_youtube.video_sitemap`` to the top of your main ``urls.py``

.. code-block::

    from djangocms_youtube.video_sitemap import CMSVideoSitemap

Add ``djangocms_youtube.views.video_sitemap`` view to your urlpatterns.

.. code-block::

    video_sitemaps = {
        'cmspages': CMSVideoSitemap,
    }

    urlpatterns = patterns(
        '',
        url(r'^videos/sitemap\.xml$', 'djangocms_youtube.views.video_sitemap', {'sitemaps': video_sitemaps })
    )

**Placeholders outside the CMS Pages**

A simple example for ``aldryn-newsblog``

.. code-block::

    ​from djangocms_youtube.video_sitemap import VideoSitemap
    from aldryn_newsblog.models import Article

    ​
    class NewsblogVideoSitemap(VideoSitemap):
        model = Article
    ​
        def get_queryset(self):
            queryset = super(NewsblogVideoSitemap, self).get_queryset()
            language = self.get_language()
            queryset = queryset.translated(language)
            return queryset.published()
    ​
        def location(self, item):
            return item.get_absolute_url(self.get_language())


You may also like...
--------------------

* djangocms-disqus - https://github.com/mishbahr/djangocms-disqus
* djangocms-forms — https://github.com/mishbahr/djangocms-forms
* djangocms-gmaps — https://github.com/mishbahr/djangocms-gmaps
* djangocms-instagram — https://github.com/mishbahr/djangocms-instagram
* djangocms-responsive-wrapper — https://github.com/mishbahr/djangocms-responsive-wrapper
* djangocms-twitter2  https://github.com/mishbahr/djangocms-twitter2
