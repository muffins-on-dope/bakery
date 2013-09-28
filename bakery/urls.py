# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^$', 'bakery.views.index', name='index'),

    url('', include('social.apps.django_app.urls', namespace='social'))
)
