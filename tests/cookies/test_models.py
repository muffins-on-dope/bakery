# -*- coding: utf-8 -*-

import httpretty

from django.utils.timezone import now
from django.utils.unittest import TestCase

from bakery.auth.models import BakeryUser
from bakery.cookies.models import Cookie
from bakery.utils.test import read


class TestCookieModel(TestCase):

    def tearDown(self):
        BakeryUser.objects.all().delete()
        Cookie.objects.all().delete()

    def test_owner_on_delete(self):
        """
        Verifies that a user is not being delete when a Cookie is deleted, but
        all Cookies a user owns are deleted when their owner is being deleted.
        """
        user = BakeryUser.objects.create_user('username', 'password')
        cookie = Cookie.objects.create(name='name', url='http://example.com/',
            owner=user, last_change=now(), last_poll=now())
        self.assertEqual(BakeryUser.objects.count(), 1)
        self.assertEqual(Cookie.objects.count(), 1)

        cookie.delete()
        self.assertEqual(BakeryUser.objects.count(), 1)
        self.assertEqual(Cookie.objects.count(), 0)

        cookie = Cookie.objects.create(name='name', url='http://example.com/',
            owner=user, last_change=now(), last_poll=now())
        user.delete()
        self.assertEqual(BakeryUser.objects.count(), 0)
        self.assertEqual(Cookie.objects.count(), 0)

    def test_attributes(self):
        user = BakeryUser.objects.create_user('username', 'password')
        cookie = Cookie.objects.create(name='FancyName', url='http://abc.de/',
            owner=user, last_change=now(), last_poll=now(), owner_name='foo')
        self.assertEqual(str(cookie), 'FancyName')
        self.assertEqual(cookie.full_name, 'foo/FancyName')

    @httpretty.activate
    def test_repository(self):
        httpretty.register_uri(httpretty.GET,
            'https://api.github.com/repos/audreyr/cookiecutter-pypackage',
            body=read(__file__, '..', '_replay_data', 'cookiecutter-pypacker-repository'),
            content_type='application/json; charset=utf-8'
        )

        user = BakeryUser.objects.create_user('username', 'password')
        cookie = Cookie.objects.create(name='cookiecutter-pypackage',
            url='https://github.com/audreyr/cookiecutter-pypackage', owner=user,
            last_change=now(), last_poll=now(), owner_name='audreyr')
        self.assertFalse(hasattr(cookie, '_repository'))
        repo = cookie.repository
        self.assertEqual(repo.id, 11407567)
        self.assertTrue(hasattr(cookie, '_repository'))
