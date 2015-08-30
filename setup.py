#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangocms_youtube

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_youtube.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='djangocms-youtube',
    version=version,
    description="""YouTube embed plugin for your django-cms powered site with options
    for custom video thumbnails, analytics, SEO and more.""",
    long_description=readme,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/djangocms-youtube',
    packages=[
        'djangocms_youtube',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf',
        'django-cms>=3.0',
        'django-filer>=0.9',
        'isodate>=0.5.4',
        'jsonfield',
        'requests',
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangocms-youtube, YouTube, django-cms, cmsplugin-youtube',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
