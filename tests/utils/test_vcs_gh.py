# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings
from django.utils.unittest import TestCase

from bakery.utils.vcs.gh import _github_setup


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
