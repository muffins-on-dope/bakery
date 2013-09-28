# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'bakery.views.index', name='index'),
    url(r'^style_demo$', 'bakery.views.style_demo', name='style_demo'),
)
