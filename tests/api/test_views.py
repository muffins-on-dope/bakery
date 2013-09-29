# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.utils.encoding import smart_str
from bakery.auth.models import BakeryUser
from bakery.cookies.models import Cookie


class TestApi(TestCase):

    def test_cookies_list_empty(self):
        resp = self.client.get('/api/v1/cookies/list/')
        self.assertEqual(resp.content, b'[]')

    def test_cookies_list(self):
        BakeryUser.objects.create_user('user')
        user = BakeryUser.objects.get(username='user')
        cookie = Cookie.objects.create(
            name='test',
            owner_name='test',
            url='http://example.com/unique',
            owner=user,
            backend='github'
        )

        resp = self.client.get('/api/v1/cookies/list/')
        data = json.loads(smart_str(resp.content))
        self.assertEqual(
            data,
            [{
                "url": "http://example.com/unique",
                "description": "",
                "name": "test",
                "last_change": None
            }]
        )
