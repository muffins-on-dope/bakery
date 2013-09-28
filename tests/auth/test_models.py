# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils import unittest
from django.utils.unittest import TestCase

from bakery.auth.models import BakeryUser


class TestBakeryUserModel(TestCase):

    def tearDown(self):
        BakeryUser.objects.all().delete()

    @unittest.skip('Not yet implemented')
    def test_get_absolute_url(self):
        user = BakeryUser.objects.create_user('user', 'password')
        user.name = 'John Doe'
        self.assertEqual(user.get_absolute_url(), reverse('user-detail-view'))

    def test_get_full_name(self):
        user = BakeryUser.objects.create_user('user', 'password')
        user.name = 'John Doe'
        self.assertEqual(user.get_full_name(), 'John Doe')

    def test_get_short_name(self):
        user = BakeryUser.objects.create_user('user', 'password')
        user.name = 'John Doe'
        self.assertEqual(user.get_short_name(), 'John Doe')
