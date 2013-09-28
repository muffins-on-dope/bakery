# -*- coding: utf-8 -*-

import httpretty

from django.core import management
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO

from bakery.auth.models import BakeryUser
from bakery.cookies.models import Cookie
from bakery.utils.test import read


class TestCommands(TestCase):

    def tearDown(self):
        BakeryUser.objects.all().delete()
        Cookie.objects.all().delete()

    def test_createsuperuser(self):
        out = StringIO()
        management.call_command('createsuperuser', 'SocialUser', stdout=out)
        self.assertIn('Created SocialUser', out.getvalue())


    def test_createsuperuser_duplicat(self):
        out = StringIO()
        management.call_command('createsuperuser', 'SocialUser', stdout=out)
        self.assertRaises(CommandError, management.call_command, ('SocialUser',))

    @httpretty.activate
    def test_importcookie(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage',
            body=read(__file__, 'replay_data', 'repository'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/users/audreyr',
            body=read(__file__, 'replay_data', 'owner'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage/contents/',
            body=read(__file__, 'replay_data', 'root_dir'),
            content_type='application/json; charset=utf-8'
        )
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage/contents/cookiecutter.json',
            body=read(__file__, 'replay_data', 'cookiecutter.json'),
            content_type='application/json; charset=utf-8'
        )
        out = StringIO()
        management.call_command('importcookie', 'https://github.com/audreyr/cookiecutter-pypackage', stdout=out)
        self.assertIn('Imported https://github.com/audreyr/cookiecutter-pypackage', out.getvalue())

    def test_importcookie_verbose(self):
        out = StringIO()
        management.call_command('importcookie', 'https://github.com/audreyr/cookiecutter-pypackage', verbosity=2, stdout=out)
        self.assertIn('Importing https://github.com/audreyr/cookiecutter-pypackage', out.getvalue())
        self.assertIn('Imported https://github.com/audreyr/cookiecutter-pypackage', out.getvalue())

    def test_importcookie_invalid_url(self):
        self.assertRaises(CommandError, management.call_command, ('importcookie',), 'http://example.com')
