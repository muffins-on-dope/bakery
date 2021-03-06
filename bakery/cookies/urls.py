# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('bakery.cookies.views',
    url(r'^cookie/add/$', 'add', name='add'),
    url(r'^cookie/(?P<owner_name>[^/]+)/(?P<name>[^/]+)/$', 'detail', name='detail'),
    url(r'^cookie/(?P<owner_name>[^/]+)/(?P<name>[^/]+)/fork/$', 'fork', name='fork'),
)
