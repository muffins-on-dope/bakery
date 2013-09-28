# -*- coding: utf-8 -*-
from bakery.settings import *

import os.path

RUNTESTS_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'tests',
)

SECRET_KEY = 'test-secret-key'

TEST_RUNNER = 'discover_runner.DiscoverRunner'
