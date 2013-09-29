# -*- coding: utf-8 -*-

import json
import pytz
import http.client

from base64 import standard_b64decode

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import make_aware

from github import Github

from bakery.cookies.exceptions import (InvalidRepositoryError,
                                       InvalidContentFileEncoding)


def _github_setup():
    """
    Sets up the server-wide Github authentication for the project and returns
    an authorized `Github object from PyGithub
    <http://jacquev6.github.io/PyGithub/github.html>`_ which can be used to
    list users, repos, etc.
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

#: Server-wide authenticated GitHub state
github_setup = _github_setup()


def get_repo_from_url(url, gh_setup=github_setup):
    """
    Given an URL like (ssh://)git@github.com/user/repo.git or any other url
    that defines the root of a repository, this function returns the PyGithub
    resource describing that object.

    One can use :func:`get_cookie_data_from_repo` or
    :func:`get_mapping_file_from_repo` to get further information about that
    repository such as the content of the ``cookiecutter.json`` file.

    :param str url: The root URL to a github repository
    :param gh_setup: If not the server-wide authentiaction :data:`github_setup`
        should be used, this parameter can be set to another, e.g. user
        authenticated PyGithub object
    :return: Returns an instance of a ``PyGithub.Repository``.
    :raises: ``InvalidRepositoryError`` if the given URL does not match a known
        GitHub URL.
    """
    if 'git@github.com' in url:
        identifier = 'git@github.com'
    elif 'https://github.com/' in url:
        identifier = 'https://github.com'
    else:
        raise InvalidRepositoryError('{0} is not a valid GitHub URL'.format(url))
    index = url.index(identifier)
    length = len(identifier)
    start = length + index + 1  # +1 for separator after identifier
    full_name = url[start:]
    if full_name.endswith('.git'):
        full_name = full_name[:-4]  # strip .git
    return get_repo_from_full_name(full_name, gh_setup)


def get_repo_from_full_name(full_name, gh_setup=github_setup):
    """
    Returns a PyGithub.Repository by a given full_name (<user>/<repo_name>)
    """
    repository = gh_setup.get_repo(full_name)
    return repository


def get_cookie_data_from_repo(repo):
    """
    Given a ``PyGithub.Repository`` instance construct a dict holding the
    following information:

    * ``name`` -- Repository name
    * ``url`` -- The HTTP URL to view the repository in a browser
    * ``description`` -- A brief description about the repository
    * ``owner_name`` -- The owner name of the repository
    * ``last_change`` -- A timezone aware timestamp of the last modification
      on the repository
    * ``mapping`` -- The content of the ``cookiecutter.json`` file (or similar)
    * ``backend`` -- 'github'
    * _``owner`` -- A dict with information about the owner of the repository

      * ``username`` -- The user- or login name (required)
      * ``email`` -- The email address of the user
      * ``name`` -- The full name
      * ``is_organization`` -- If the repository is owned by a orga: ``True``
      * ``profile_url`` -- The HTTP URL to view the user in a browser

    :param repo: A ``PyGithub.Repository`` instance
    :return dict: The dict containing Cookie and BakeryUser information
    :raises: ``InvalidRepositoryError`` if no mapping file can be found in the
        given repository
    :raises: ``InvalidContentFileEncoding`` if the content of the given file
        cannot be parsed.
    """
    mapping_file = get_mapping_file_from_repo(repo)
    content = get_content_from_content_file(mapping_file)

    owner = repo.owner
    owner_data = {
        'username': owner.login,
        'email': owner.email,
        'name': owner.name,
        'is_organization': owner.type == "Organization",
        'profile_url': owner.html_url,
    }

    # TODO: I think this should not fail like that :-/
    try:
        participants = ', '.join(user.login for user in repo.get_contributors())
    except http.client.BadStatusLine:
        participants = None

    data = {
        'name': repo.name,
        'owner_name': repo.owner.login,
        'url': repo.html_url,
        'description': repo.description,
        'last_change': make_aware(repo.updated_at, pytz.UTC),
        'mapping': content,
        'backend': 'github',
        'repo_watchers': repo.watchers,
        'repo_forks': repo.forks,
        'participants': participants,
        'language': repo.language,
        'homepage': repo.homepage,
        'clone_urls': {
            'ssh': repo.ssh_url,
            'git': repo.git_url,
        },
        '_owner': owner_data,
    }
    return data


def filter_repo(repo, filters):
    contents = repo.get_contents('/')
    if contents:
        candidates = {}
        for rd in contents.raw_data:
            if rd['type'] != 'file':
                continue
            for key, filter in filters.items():
                if filter(rd[key]):
                    candidates[rd['name']] = rd

    return candidates


def get_mapping_file_from_repo(repo):
    """
    Finds a ``cookiecutter.json`` or another JSON file in the repository root
    and treat it as the mapping file.

    The candidate selection works as follows:
    #. All files ending with ``.json`` on the root-level will be added to a candidate set.
    #. If now candidates have been found raise ``InvalidRepositoryError``
    #. If more than one candidate has been found:

       #. if there is a ``cookiecutter.json`` in the candidate list, use it
       #. Otherwise raise ``InvalidRepositoryError``

    #. Return there is exactly one ``JSON`` file: use it
    #. If a mapping_file has been found, open it as a ``PyGithub.ContentFile``
       and return the content_file

    :raises: ``InvalidRepositoryError`` if there was no way to
        deterministically find the mapping file.
    """
    candidates = filter_repo(repo, {'name': lambda val: val.endswith('.json')})

    if not candidates:
        raise InvalidRepositoryError('No JSON mapping file found!')

    if len(candidates) > 1:
        mapping_file = candidates.get('cookiecutter.json', None)
        if mapping_file is None:
            raise InvalidRepositoryError('Cannot decide for a mapping file! '
                                         'Multiple files found: {0}'.format(', '.join(candidates.keys)))
    else:
        mapping_file = list(candidates.values())[0]
    return repo.get_contents('/' + mapping_file['name'])


def decode_file(content_file):
    """
    Given a ``PyGithub.ContentFile`` this function will decode the file's data.

    :return dict: Returns a raw decoded string.
    :raises: ``InvalidContentFileEncoding`` raised if not suitable decoding
        is defined.
    """
    decoded = None
    if content_file.encoding == 'base64':
        decoded = standard_b64decode(content_file.content).decode('utf-8')
    if decoded is None:
        raise InvalidContentFileEncoding(
            'Encoding {0} cannot be decoded'.format(content_file.encoding))
    return decoded


def get_content_from_content_file(content_file):
    """
    Given a ``PyGithub.ContentFile`` this function will decode the file's data
    and loads it's JSON content.

    :return dict: Returns a ``dict`` with the JSON content
    :raises: ``InvalidContentFileEncoding`` raised if not suitable decoding
        is defined.
    """
    return json.loads(decode_file(content_file))


def fork_repository(user, repo):
    """
    Forks the repository ``repo`` to the user ``user``.

    :return: Returns an instance of the newly forked ``PyGithub.Repository``.
    """
    return user.create_fork(repo)
