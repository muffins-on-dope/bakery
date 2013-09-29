# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('bakery.socialize.views',
    url(r'^vote/$', 'vote', name='vote'),
    url(r'^unvote/$', 'vote', {'unvote': True}, name='unvote'),
    url(r'^votes/(?P<pk>\d+)/$', 'votes_for_cookie', name='votes_for_cookie'),
    url(r'^voted/(?P<pk>\d+)/$', 'votes_by_user', name='votes_by_user'),
)
