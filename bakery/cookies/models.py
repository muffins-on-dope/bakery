# -*- coding: utf-8 -*-

import json
import re

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from bakery.auth.models import BakeryUser
from bakery.cookies.managers import CookieManager
from bakery.utils.vcs.gh import (fork_repository, get_cookie_data_from_repo,
                                 get_repo_from_full_name)


_punctuation = re.compile(r'[!,.:;?]*')

ACTIVITY = {
    'ancient': 0,
    'moderate': 1,
    'active': 2
}


class Cookie(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    owner_name = models.CharField(_('Owner name'), max_length=50)
    url = models.URLField(_('URL'), unique=True)
    owner = models.ForeignKey(get_user_model(), verbose_name=_('User'),
                              on_delete=models.CASCADE)
    description = models.TextField(_('Description'), blank=True)
    last_change = models.DateTimeField(_('Last change'), null=True)
    last_poll = models.DateTimeField(_('Last poll'), null=True)
    backend = models.CharField(_('Backend'), max_length=25)
    mapping = JSONField(default={})

    # Hosting Statistics
    license = models.CharField(_('License'), max_length=50, blank=True)
    repo_watchers = models.IntegerField(_("repo watchers"), default=0)
    repo_forks = models.IntegerField(_("repo forks"), default=0)
    participants = models.TextField(_("Participants"),
        help_text="List of collaborats/participants on the project", null=True)
    language = models.CharField(_('Language'), max_length=50, null=True)
    homepage = models.CharField(_('Homepage'), max_length=255, null=True)
    clone_urls = JSONField(default={})

    # Social aspect, such as votes etc
    votes = models.ManyToManyField(BakeryUser, through='socialize.Vote',
        related_name='votes')

    objects = CookieManager()

    class Meta:
        ordering = ['-last_change', 'name']
        unique_together = ('name', 'owner_name')
        verbose_name = _('Cookie')
        verbose_name_plural = _('Cookies')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # TODO
        return ''

    @property
    def full_name(self):
        return "{0}/{1}".format(self.owner_name, self.name)

    @property
    def short_description(self):
        descr = self.mapping.get('project_short_description', None)
        if descr is None:
            descr = self.description
        return _punctuation.split(descr)[0]

    @property
    def activity(self):
        if self.last_change >= (datetime.utcnow() - timedelta(days=365)):
            return ACTIVITY['ancient']
        elif self.last_change >= (datetime.utcnow() - timedelta(days=10)):
            return ACTIVITY['moderate']
        else:
            return ACTIVITY['active']

    def fork(self, user):
        """
        :raises: ``UnknownObjectException`` is raised if the repository cannot
            be located.
        """
        fork = fork_repository(user, self.repository)
        cookie_dict = get_cookie_data_from_repo(fork)
        owner_dict = cookie_dict.pop('_owner', None)
        Cookie.objects.import_from_cookie_dict(
            cookie_dict,
            owner_dict,
            self.repository
        )

    @property
    def repository(self):
        repository = getattr(self, '_repository', None)
        if not repository:
            repository = get_repo_from_full_name(self.full_name)
            setattr(self, '_repository', repository)
        return repository

    @property
    def mapping_pretty(self):
        mapping_pretty = getattr(self, '_mapping_pretty', None)
        if not mapping_pretty:
            mapping_pretty = json.dumps(self.mapping, ensure_ascii=False,
                                        indent=4, sort_keys=True)
            setattr(self, '_mapping_pretty', mapping_pretty)
        return mapping_pretty

    @property
    def clone_urls_tuple(self):
        return sorted(tuple(self.clone_urls.items()))
