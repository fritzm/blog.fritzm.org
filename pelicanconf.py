#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Fritz Mueller'
SITENAME = 'fritzm.github.io'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('facebook', 'http://facebook.com/fritzmueller'),
	      ('twitter', 'http://twitter.com/infrafritz'),
	      ('Instagram', 'http://instagram.com/infrafritz'),
	      ('LinkedIn', 'http://www.linkedin.com/pub/fritz-mueller/a/679/62/'),
          ('JSFiddle', 'http://jsfiddle.net/user/fritzm/fiddles/'),
	      ('GitHub', 'https://github.com/fritzm'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins', 'plugins-local']
PLUGINS = ['render_math', 'thumbnailer', 'liquid_tags.youtube', 'photoswipe']
THEME = './theme'
SLUGIFY_SOURCE = 'basename'

OUTPUT_RETENTION = (".git*")

IMAGE_PATH = "images"
THUMBNAIL_SIZES = { 'thumbnail_tall': '?x200' }
THUMBNAIL_DIR = "images"
