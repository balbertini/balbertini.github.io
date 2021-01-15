#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Bruno Albertini'
SITENAME = 'Site do Bruno Albertini'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'


PLUGIN_PATHS = ["../pelican-plugins"]
# PLUGINS = ['i18n_subsites', 'render_math', 'post_stats', 'jinja2content']
PLUGINS = ['i18n_subsites', 'render_math', 'post_stats', 'filetime_from_git', 'jinja2content']
# Processors extensions
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n']
}
JINJA2CONTENT_TEMPLATES=['../templates']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums':'True',
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
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

DEFAULT_PAGINATION = 10

STATIC_PATHS = [
    'images',
    'extra',
]


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme related customization
THEME = 'pelican_theme_flex'
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
