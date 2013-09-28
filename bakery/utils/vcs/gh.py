# -*- coding: utf-8 -*-

import pytz

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import make_aware

from github import Github

from bakery.auth.models import BakeryUser


def _github_setup():
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

github_setup = _github_setup()


def get_repo_from_url(url):
    if 'git@github.com' in url:
        identifier = 'git@github.com'
    elif 'https://github.com/' in url:
        identifier = 'https://github.com'
    else:
        raise ValueError('{0} is not a valid GitHub URL')
    index = url.index(identifier)
    length = len(identifier)
    start = length + index + 1  # +1 for separator after identifier
    path = url[start:]
    username, repo = path.split('/', 1)
    if repo.endswith('.git'):
        repo = repo[:-4]  # strip .git
    user = github_setup.get_user(username)
    repository = user.get_repo(repo)
    return repository


def get_cookie_data_from_repo(repo):
    is_organization = repo.organization is not None
    username = repo.owner.login
    owner = BakeryUser.objects.get_or_create(
        username=username,
        is_organization=is_organization
    )
    owner = owner[0]  # We don't care if the owner has been created or not
    data = {
        'name': repo.name,
        'url': repo.html_url,
        'owner': owner,
        'description': repo.description,
        'last_change': make_aware(repo.updated_at, pytz.UTC),
    }
    return data
