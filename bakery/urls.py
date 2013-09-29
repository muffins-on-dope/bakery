# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'bakery.views.home', name='home'),
    url(r'^logout/$', 'bakery.views.logout', name='logout'),
    url(r'^styles/$', 'bakery.views.styles', name='styles'),
    url(r'^login-error/$', 'bakery.views.login_error', name='login_error'),

    url(r'^', include('bakery.cookies.urls', namespace='cookies')),
    url(r'^', include('bakery.socialize.urls', namespace='socialize')),
    url('api/v1/', include('bakery.api.urls', namespace='api')),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.login_template = 'admin/custom_login.html'
