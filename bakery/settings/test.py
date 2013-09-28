# -*- coding: utf-8 -*-

from bakery.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
    }
}

INSTALLED_APPS = INSTALLED_APPS + ('tests',)

TEST_RUNNER = 'discover_runner.DiscoverRunner'

GITHUB_CREDENTIALS = {}
