#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = 'Bruno Albertini'
SITENAME = "B.Albertini's site"
SITETITLE = 'B.Albertini'
SITESUBTITLE = 'Professor'
# SITELOGO = SITEURL + 'content/images/profile.png'
# FAVICON = SITEURL + 'content/images/favicon.ico'
SITEURL = ''
SITELOGO = SITEURL + '/images/profile.png'
FAVICON = SITEURL + '/images/favicon.ico'
THEME = 'theme'
PATH = 'content'
# CUSTOM_CSS = 'static/academicons.min.css'

BROWSER_COLOR = '#333'
ROBOTS = 'index, follow'

TIMEZONE = 'America/Sao_Paulo'

PLUGIN_PATHS = ["../pelican-plugins"]
# Enable i18n plugin, probably you already have some others here.
PLUGINS = ['i18n_subsites', 'render_math', 'post_stats']
# Enable Jinja2 i18n extension used to parse translations.
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n'],}

# DEFAULT_LANG = u'pt_BR'
DATE_FORMATS = {
    'en_US': '%a, %d %b %Y',
    'pt_BR': '%d/%m/%Y (%a)',
}

# Default theme language.
I18N_TEMPLATES_LANG = 'pt_BR'
DEFAULT_LANG = 'pt_BR'
# Your language.
OG_LOCALE = 'pt_BR'
LOCALE = ('pt_BR','pt_BR.UTF-8','en_US','en_US.UTF-8')
# LOCALE = ('pt_BR.utf8', 'en_US.utf8')

# Default theme language.
I18N_TEMPLATES_LANG = "pt_BR"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()
         # ('Pelican', 'http://getpelican.com/'),
         # ('Python.org', 'http://python.org/'),
         # ('Jinja2', 'http://jinja.pocoo.org/'),
         # ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/balbertini'),
    ('rss', '//balbertini.github.io/feeds/all.atom.xml'),
)

DEFAULT_PAGINATION = 10

STATIC_PATHS = [
    'images',
    # 'extra/robots.txt',
    'extra/favicon.ico',
    'extra',
    # 'static',
]

EXTRA_PATH_METADATA = {
    # 'extra/robots.txt': {'path': 'robots.txt'},
    # 'extra/custom.css': {'path': 'static/custom.css'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}
COPYRIGHT_NAME = "Bruno Albertini"
COPYRIGHT_YEAR = 2014
