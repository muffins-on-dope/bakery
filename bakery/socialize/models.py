# -*- coding: utf-8 -*-

from django.db import models

from bakery.socialize.managers import VoteManager


class Vote(models.Model):
    cookie = models.ForeignKey('cookies.Cookie')
    user = models.ForeignKey('auth.BakeryUser')

    datetime = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'cookie')

    def __repr__(self):
        return '<Vote: cookie: {0}, user: {1}>'.format(self.cookie, self.user)
