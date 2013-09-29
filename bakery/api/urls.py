# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('bakery.api.views',
    url(r'^cookies/list/$', 'cookies_list'),
    url(r'^cookies/list/(?P<page>\d+)/$', 'cookies_list'),
    url(r'^cookies/search/(?P<term>[^/]+)/$', 'cookies_search'),
    url(r'^cookies/new/$', 'cookies_new'),
)
