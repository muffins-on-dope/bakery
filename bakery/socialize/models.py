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


CANDIES = (
    ('rice-cracker', _('Rice Cracker'), '&#x1f358;'),
    ('candy', _('Candy'), '&#1f36c;'),
    ('lollipop', _('Lollipop'), '&#1f36d;'),
    ('chocolate-bar', _('Chocolate Bar'), '&#x1f36b;'),
    ('doughnut', _('Doughnut'), '&#x1f369;'),
    ('cookie', _('Cookie'), '&#x1f36a;'),
)
CANDY_CHOICES = ((candy[0], candy[1]) for candy in CANDIES)
CANDY_LABELS = dict(CANDY_CHOICES)
CANDY_PICTOGRAM = dict((candy[0], candy[2]) for candy in CANDIES)


class Candy(models.Model):
    candy_type = models.CharField(_('Candy'), choices=CANDY_CHOICES, max_length=25)
    user = models.ForeignKey('auth.BakeryUser', related_name='candies')
    vote = models.ForeignKey(Vote, null=True, on_delete=models.CASCADE)

    datetime = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return '<Candy: candy: {0}, user: {1}>'.format(self.candy_type, self.user)
