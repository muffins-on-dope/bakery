# -*- coding: utf-8 -*-

from django.db import models

from bakery.auth.models import BakeryUser
from bakery.cookies.models import Cookie


class Vote(models.Model):
    user = models.ForeignKey(BakeryUser)
    cookie = models.ForeignKey(Cookie)
    datetime = models.DateTimeField(auto_now_add=True)
