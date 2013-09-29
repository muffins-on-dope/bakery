# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^logout/$', 'bakery.views.logout', name='logout'),
    url(r'^login-error/$', 'bakery.views.login_error', name='login_error'),

    url(r'^profile/(?P<username>.*?)/$', 'bakery.views.profile', name='profile'),
)
