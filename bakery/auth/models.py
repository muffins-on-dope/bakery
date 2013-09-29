# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

from bakery.auth.managers import BakeryUserManager


class BakeryUser(AbstractBaseUser):
    username = models.CharField(_('Username'), max_length=50, unique=True)
    email = models.EmailField(_('Email'), max_length=254, unique=True)
    name = models.CharField(_('Name'), max_length=100, blank=True, null=True)
    is_superuser = models.BooleanField(_('Superuser'), default=False)
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    is_organization = models.BooleanField(_('Organization'))
    profile_url = models.URLField(_('Profile'), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = BakeryUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        # TODO
        return NotImplementedError

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name
