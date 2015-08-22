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


High resolution thumbnail
=========================

Fetches the highest resolution thumbnail available from YouTube for a given video with options for custom video thumbnails using ``django-filer``.

.. image:: http://mishbahr.github.io/assets/djangocms-youtube/thumbnail/djangocms-youtube-001.png
  :target: http://mishbahr.github.io/assets/djangocms-youtube/djangocms-youtube-001.png
  :width: 768px
  :align: center


**Note:** On desktop, the Image Overlay becomes a play button. Clicking the image starts the video. Mobile devices require two taps to play the video. Tap the image once to remove it and display the video player. Then, tap the play button to begin the video.


Schema.org integration
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

Plugin can have child plugins (i.e  other plugins placed inside this plugin), rendered as an overlay, when the video finishes.

You can disable this functionality by overriding ``DJANGOCMS_YOUTUBE_ALLOW_CHILDREN`` in your ``settings.py`` file

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


You may also like...
--------------------

* djangocms-forms — https://github.com/mishbahr/djangocms-forms
* djangocms-gmaps — https://github.com/mishbahr/djangocms-gmaps
* djangocms-instagram — https://github.com/mishbahr/djangocms-instagram
* djangocms-responsive-wrapper — https://github.com/mishbahr/djangocms-responsive-wrapper
* djangocms-twitter2  https://github.com/mishbahr/djangocms-twitter2
