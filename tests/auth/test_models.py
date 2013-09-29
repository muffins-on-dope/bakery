# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import unittest

from bakery.auth.models import BakeryUser


class TestBakeryUserModel(TestCase):

    def test_get_absolute_url(self):
        user = BakeryUser.objects.create_user('user', 'password')
        user.name = 'John Doe'
        self.assertEqual(user.get_absolute_url(),
                         reverse('auth:profile', kwargs={'username': 'user'}))

    def test_get_full_name(self):
        user = BakeryUser.objects.create_user('user', 'password')
        user.name = 'John Doe'
        self.assertEqual(user.get_full_name(), 'John Doe')

    def test_get_short_name(self):
        user = BakeryUser.objects.create_user('user', 'password')
        user.name = 'John Doe'
        self.assertEqual(user.get_short_name(), 'John Doe')
