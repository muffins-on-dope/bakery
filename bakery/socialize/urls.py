# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('bakery.socialize.views',
    url(r'^vote/$', 'vote', name='vote'),
    # url(r'^votes/(?P<id>\d+)/$', 'votes_for_cookie', name='votes_for_cookie'),
    # url(r'^voted/(?P<id>\d+)/$', 'votes_by_user', name='votes_by_user'),
)
