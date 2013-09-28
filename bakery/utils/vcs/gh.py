# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from github import Github


def github_setup():
    """
    Setup the Github authentication and returns an authorized `Github object
    from PyGithub <http://jacquev6.github.io/PyGithub/github.html>`_
    """

    credentials = getattr(settings, 'GITHUB_CREDENTIALS', None)

    if credentials is None:
        raise ImproperlyConfigured('No GITHUB_CREDENTIALS set')

    # Verify that only allowed keys are passed
    allowed_keys = set(['login_or_token', 'password', 'client_id', 'client_secret'])
    given_keys = set(credentials.keys())
    forbidden_keys = given_keys - allowed_keys
    if given_keys - allowed_keys:
        raise ImproperlyConfigured('Invalid keys in GITHUB_CREDENTIALS: '
            '{0}'.format(','.join(forbidden_keys)))

    if 'password' in credentials and not 'login_or_token' in credentials:
        raise ImproperlyConfigured('You need to define the login_or_token to '
           'use password authentiaction in GITHUB_CREDENTIALS')

    if 'client_secret' in credentials and not 'client_id' in credentials:
        raise ImproperlyConfigured('You need to define the client_id to '
           'use client_secret authentiaction in GITHUB_CREDENTIALS')

    if 'client_id' in credentials and not 'client_secret' in credentials:
        raise ImproperlyConfigured('You need to define the client_secret to '
           'use client_id authentiaction in GITHUB_CREDENTIALS')

    return Github(**credentials)

github = github_setup()
