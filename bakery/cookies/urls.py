# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('bakery.cookies.views',
    url(r'^cookie/(?P<owner_name>[^/]+)/(?P<name>[^/]+)/$', 'detail', name='detail'),
)
