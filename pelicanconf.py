#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Fritz Mueller'
SITENAME = u'fritzm.github.io'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('facebook', 'http://facebook.com/fritzmueller'),
	      ('twitter', 'http://twitter.com/infrafritz'),
	      ('Instagram', 'http://instagram.com/infrafritz'),
	      ('LinkedIn', 'http://www.linkedin.com/pub/fritz-mueller/a/679/62/'),
          ('JSFiddle', 'http://jsfiddle.net/user/fritzm/fiddles/'),
	      ('GitHub', 'https://github.com/fritzm'),)

SUMMARY_MAX_LENGTH = None
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins']
PLUGINS = ['render_math', 'image_process']
THEME = './theme'
SLUGIFY_SOURCE = 'basename'

OUTPUT_RETENTION = (".git*")

IMAGE_PROCESS = {
    'article-image': ["scale_in 300 300 True"],
    'thumb': ["scale_in 250 250 False"],
}
