# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'bakery.views.home', name='home'),
    url(r'^styles/$', 'bakery.views.styles', name='styles'),

    url(r'^', include('bakery.auth.urls', namespace='auth')),
    url(r'^', include('bakery.cookies.urls', namespace='cookies')),
    url(r'^', include('bakery.socialize.urls', namespace='socialize')),
    url('api/v1/', include('bakery.api.urls', namespace='api')),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.login_template = 'admin/custom_login.html'
