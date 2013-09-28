# -*- coding: utf-8 -*-

import json
import pytz

from base64 import standard_b64decode

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import make_aware

from github import Github

from bakery.cookies.exceptions import (InvalidRepositoryError,
    InvalidContentFileEncoding)


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
    mapping_file = get_mapping_file_from_repo(repo)
    content = get_content_from_content_file(mapping_file)

    owner = repo.owner
    owner_data = {
        'username': owner.login,
        'email': owner.email,
        'name': owner.name,
        'is_organization': repo.organization is not None,
        'profile_url': owner.html_url,
    }
    data = {
        'name': repo.name,
        'url': repo.html_url,
        'description': repo.description,
        'last_change': make_aware(repo.updated_at, pytz.UTC),
        'mapping': content,
        '_owner': owner_data,
    }
    return data


def get_mapping_file_from_repo(repo):
    contents = repo.get_contents('/')
    if contents:
        candidates = {}
        for rd in contents.raw_data:
            if rd['type'] != 'file':
                continue
            if rd['name'].endswith('.json'):
                candidates[rd['name']] = rd

        if not candidates:
            raise InvalidRepositoryError('No JSON mapping file found!')
        if len(candidates) > 1:
            if 'cookiecutter.json' in candidates:
                mapping_file = rd
            else:
                raise InvalidRepositoryError('Cannot decide for a mapping file! '
                    'Multiple files found: {0}'.format(', '.join(candidates.keys)))
        else:
            mapping_file = list(candidates.values())[0]
        return repo.get_contents(mapping_file['name'])
    raise InvalidRepositoryError('The repository does not have any content!')


def get_content_from_content_file(content_file):
    decoded = None
    if content_file.encoding == 'base64':
        decoded = standard_b64decode(content_file.content).decode('utf-8')
    if decoded is None:
        raise InvalidContentFileEncoding(
            'Encoding {0} cannot be decoded'.format(content_file.encoding))
    mapping_data = json.loads(decoded)
    return mapping_data
