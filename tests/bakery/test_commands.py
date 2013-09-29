# -*- coding: utf-8 -*-

import httpretty

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO

from bakery.auth.models import BakeryUser
from bakery.utils.test import read


class TestCommands(TestCase):

    def test_makesuperuser(self):
        BakeryUser.objects.create_user('SocialUser')
        user = BakeryUser.objects.get(username='SocialUser')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        out = StringIO()
        management.call_command('makesuperuser', 'SocialUser', stdout=out)
        self.assertIn('Updated SocialUser to superuser status', out.getvalue())
        user = BakeryUser.objects.get(username='SocialUser')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_makesuperuser_not_found(self):
        BakeryUser.objects.create_user('SocialUser')
        user = BakeryUser.objects.get(username='SocialUser')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertRaises(CommandError, management.call_command, ('makesuperuser',), 'SocialUser2')

    @httpretty.activate
    def test_importcookie(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-repository'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/users/audreyr',
            body=read(__file__, '..', '_replay_data', 'audreyr'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage/contents/',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-rootdir'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage/contents/cookiecutter.json',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-cookiecutter.json'),
            content_type='application/json; charset=utf-8'
        )
        out = StringIO()
        management.call_command('importcookie', 'https://github.com/audreyr/cookiecutter-pypackage', stdout=out)
        self.assertIn('Imported https://github.com/audreyr/cookiecutter-pypackage', out.getvalue())

    @httpretty.activate
    def test_importcookie_verbose(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-repository'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/users/audreyr',
            body=read(__file__, '..', '_replay_data', 'audreyr'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage/contents/',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-rootdir'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage/contents/cookiecutter.json',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-cookiecutter.json'),
            content_type='application/json; charset=utf-8'
        )
        out = StringIO()
        management.call_command('importcookie', 'https://github.com/audreyr/cookiecutter-pypackage', verbosity=2, stdout=out)
        self.assertIn('Importing https://github.com/audreyr/cookiecutter-pypackage', out.getvalue())
        self.assertIn('Imported https://github.com/audreyr/cookiecutter-pypackage', out.getvalue())

    def test_importcookie_invalid_url(self):
        self.assertRaises(CommandError, management.call_command, ('importcookie',), 'http://example.com')
