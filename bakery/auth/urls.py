# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('bakery.auth.views',
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^login-error/$', 'login_error', name='login_error'),
    url(r'^profile/(?P<username>.*?)/$', 'profile', name='profile'),
)
