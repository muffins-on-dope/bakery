# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^$', 'bakery.views.index', name='index'),
    url(r'^style_demo/$', 'bakery.views.style_demo', name='style_demo'),

    url('', include('social.apps.django_app.urls', namespace='social'))
)
