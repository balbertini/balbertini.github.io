#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# from __future__ import unicode_literals

AUTHOR = 'Bruno Albertini'
SITENAME = "B.Albertini's site"
# SITETITLE = 'B.Albertini'
# SITESUBTITLE = 'Professor'
SITEURL = ''
SITELOGO = SITEURL + '/images/profile.png'
FAVICON = SITEURL + '/images/favicon.ico'
THEME = 'theme'
PATH = 'content'
# CUSTOM_CSS = 'static/academicons.min.css'

# BROWSER_COLOR = '#333'
# ROBOTS = 'index, follow'

# THEME_COLOR = 'light'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True
PYGMENTS_STYLE = 'emacs'
PYGMENTS_STYLE_DARK = 'monokai'
# MD_EXTENSIONS = ['codehilite(css_class=highlight, linenums=True)','extra']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': 'True'
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

TIMEZONE = 'America/Sao_Paulo'

PLUGIN_PATHS = ["/home/balbertini/GIT/sitePessoal/pelican-plugins"]
#PLUGIN_PATHS = ["../pelican-plugins"]
PLUGINS =  ['post_stats','render_math','jinja_filters']
PLUGINS += ['jinja2content']
# Processors extensions
# JINJA_ENVIRONMENT = {
#     'extensions': ['jinja2.ext.i18n']
# }
JINJA2CONTENT_TEMPLATES=['../templates']

# Localization
DEFAULT_LANG = 'pt_br'
I18N_TEMPLATES_LANG = "pt_BR" # For theme
LOCALE = ('pt_BR','pt_BR.utf8')
OG_LOCALE = "pr_BR"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# DEFAULT_PAGINATION = False
DEFAULT_PAGINATION = 10

STATIC_PATHS = [
    'images',
#     # 'extra/robots.txt',
    'extra/favicon.ico',
    'extra',
#     # 'static',
]

# EXTRA_PATH_METADATA = {
#     # 'extra/robots.txt': {'path': 'robots.txt'},
#     # 'extra/custom.css': {'path': 'static/custom.css'},
#     'extra/favicon.ico': {'path': 'favicon.ico'}
# }

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme related customization
THEME = '../pelican_theme_flex'
FAVICON = SITEURL + '/images/favicon.ico'
SITETITLE = 'B.Albertini'
SITESUBTITLE = 'Professor'
SITELOGO = SITEURL + '/images/profile.png'
CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version': '4.0',
    'slug': 'by-sa'
}
COPYRIGHT_NAME = "Bruno Albertini"
COPYRIGHT_YEAR = 2014
THEME_COLOR = 'light'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True
BROWSER_COLOR = "#333"
ROBOTS = "index, follow"
# For highlight.js
PYGMENTS_STYLE = 'emacs'
PYGMENTS_STYLE_DARK = 'monokai'

# Social widget
SOCIAL = (
    ('github', 'https://github.com/balbertini'),
    ('rss', '//balbertini.github.io/feeds/all.atom.xml'),
)

# LOAD_CONTENT_CACHE = True
LOAD_CONTENT_CACHE = False
# CACHE_CONTENT = True
