# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from bakery.cookies.managers import CookieManager


class Cookie(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    url = models.URLField(_('URL'))
    owner = models.ForeignKey(get_user_model(), verbose_name=_('User'),
        on_delete=models.CASCADE)
    description = models.TextField(_('Description'), default='')
    license = models.CharField(_('License'), max_length=50, default='')
    last_change = models.DateTimeField(_('Last change'), null=True)
    last_poll = models.DateTimeField(_('Last poll'), null=True)
    mapping = JSONField(default={})

    objects = CookieManager()

    class Meta:
        verbose_name = _('Cookie')
        verbose_name_plural = _('Cookies')

    def __unicode__(self):
        return self.name
