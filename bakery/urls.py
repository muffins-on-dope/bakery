# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^$', 'bakery.views.index', name='index'),
    url('api/v1/', include('bakery.api.urls')),

    url('', include('social.apps.django_app.urls', namespace='social'))
)
