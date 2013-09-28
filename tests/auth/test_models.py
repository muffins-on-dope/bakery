# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils import unittest
from django.utils.unittest import TestCase

from bakery.auth.models import BakeryUser


class TestBakeryUserManager(TestCase):

    def tearDown(self):
        BakeryUser.objects.all().delete()

    def test__create_user(self):
        user = BakeryUser.objects._create_user('user', 'password1',
            'mail@example.com', 'John Doe', is_superuser=False,
            is_staff=True, is_organization=True,
            profile_url='http://github.com/example')
        self.assertEqual(user.username, 'user')
        self.assertNotEqual(user.password, 'password1')
        self.assertEqual(user.email, 'mail@example.com')
        self.assertEqual(user.name, 'John Doe')
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_organization, True)
        self.assertEqual(user.profile_url, 'http://github.com/example')

    def test_create_user(self):
        user = BakeryUser.objects.create_user('user', 'password2')
        self.assertEqual(user.username, 'user')
        self.assertNotEqual(user.password, 'password2')
        self.assertEqual(user.email, None)
        self.assertEqual(user.name, None)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_organization, False)
        self.assertEqual(user.profile_url, '')

    def test_create_superuser(self):
        user = BakeryUser.objects.create_superuser('admin', 'password3')
        self.assertEqual(user.username, 'admin')
        self.assertNotEqual(user.password, 'password3')
        self.assertEqual(user.email, None)
        self.assertEqual(user.name, None)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_organization, False)
        self.assertEqual(user.profile_url, '')


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
