# -*- coding: utf-8 -*-

import httpretty

from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings
from django.utils.unittest import TestCase

from bakery.cookies.exceptions import InvalidRepositoryError
from bakery.utils.test import read
from bakery.utils.vcs.gh import _github_setup, get_repo_from_url


class TestGithub(TestCase):

    @override_settings(GITHUB_CREDENTIALS=None)
    def test_github_credentials_none(self):
        self.assertRaises(ImproperlyConfigured, _github_setup)

    @override_settings(GITHUB_CREDENTIALS={'something': 'value'})
    def test_github_credentials_invalid_key(self):
        self.assertRaises(ImproperlyConfigured, _github_setup)

    @override_settings(GITHUB_CREDENTIALS={'something': 'value', 'password': 'foo'})
    def test_github_credentials_invalid_key2(self):
        self.assertRaises(ImproperlyConfigured, _github_setup)

    @override_settings(GITHUB_CREDENTIALS={'password': 'foo'})
    def test_github_credentials_missing_login(self):
        self.assertRaises(ImproperlyConfigured, _github_setup)

    @override_settings(GITHUB_CREDENTIALS={'client_id': 'foo'})
    def test_github_credentials_missing_client_secret(self):
        self.assertRaises(ImproperlyConfigured, _github_setup)

    @override_settings(GITHUB_CREDENTIALS={'client_secret': 'foo'})
    def test_github_credentials_missing_client_id(self):
        self.assertRaises(ImproperlyConfigured, _github_setup)

    @httpretty.activate
    def test_get_repo_ssh_url(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/muffins-on-dope/bakery',
            body=read(__file__, 'replay_data', 'github--repository'),
            content_type='application/json; charset=utf-8'
        )
        repo = get_repo_from_url('git@github.com:muffins-on-dope/bakery')
        self.assertEqual(repo.full_name, 'muffins-on-dope/bakery')

    @httpretty.activate
    def test_get_repo_ssh_url_git(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/muffins-on-dope/bakery',
            body=read(__file__, 'replay_data', 'github--repository'),
            content_type='application/json; charset=utf-8'
        )
        repo = get_repo_from_url('git@github.com:muffins-on-dope/bakery.git')
        self.assertEqual(repo.full_name, 'muffins-on-dope/bakery')

    @httpretty.activate
    def test_get_repo_https_url(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/muffins-on-dope/bakery',
            body=read(__file__, 'replay_data', 'github--repository'),
            content_type='application/json; charset=utf-8'
        )
        repo = get_repo_from_url('https://github.com/muffins-on-dope/bakery')
        self.assertEqual(repo.full_name, 'muffins-on-dope/bakery')

    def test_get_repo_invalid_url(self):
        self.assertRaises(InvalidRepositoryError,
            get_repo_from_url, 'https://example.com/')
