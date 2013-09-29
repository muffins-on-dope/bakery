# -*- coding: utf-8 -*-

import httpretty
import json

from django.test import TestCase
from django.utils.encoding import smart_str
from bakery.auth.models import BakeryUser

from bakery.cookies.models import Cookie
from bakery.utils.test import read


class TestApi(TestCase):

    def test_cookies_list_empty(self):
        resp = self.client.get('/api/v1/cookies/list/')
        self.assertEqual(resp.content, b'[]')

    def test_cookies_list(self):
        BakeryUser.objects.create_user('user')
        user = BakeryUser.objects.get(username='user')
        Cookie.objects.create(
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

    @httpretty.activate
    def test_cookie_register(self):
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

        self.client.post('/api/v1/cookies/new/',
            json.dumps({'url': 'git@github.com/audreyr/cookiecutter-pypackage.git'}),
            content_type='application/json',
        )

        self.assertEqual(Cookie.objects.count(), 1)
