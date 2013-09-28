# -*- coding: utf-8 -*-

from django.utils.timezone import now
from django.utils.unittest import TestCase

from bakery.auth.models import BakeryUser
from bakery.cookies.models import Cookie


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
