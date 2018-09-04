#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Bruno Albertini'
SITENAME = u"B.Albertini's site"
SITEURL = ''
THEME = 'theme'

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'

PLUGIN_PATHS = ["/Users/balbertini/GIT/sitePessoal/pelican-plugins"]
# Enable i18n plugin, probably you already have some others here.
PLUGINS = ['i18n_subsites']
# Enable Jinja2 i18n extension used to parse translations.
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

DEFAULT_LANG = u'pt_BR'
# DEFAULT_LANG = u'pt_BR'
LOCALE = ('pt_BR','pt_BR.UTF-8','en_US','en_US.UTF-8')
DATE_FORMATS = {
    'en_US': '%a, %d %b %Y',
    'pt_BR': '%d/%m/%Y (%a)',
}

# Default theme language.
I18N_TEMPLATES_LANG = 'pt_BR'
# Your language.
OG_LOCALE = 'pt_BR'
LOCALE = 'pt_BR'

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
SOCIAL = ()
          # ('You can add links in your config file', '#'),
          # ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = [
    'images',
    # 'extra/robots.txt',
    'extra/favicon.ico'
]

EXTRA_PATH_METADATA = {
    # 'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
