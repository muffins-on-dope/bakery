# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield import JSONField

from bakery.cookies.managers import CookieManager
from bakery.utils.vcs.gh import (fork_repository, get_cookie_data_from_repo,
                                 get_repo_from_full_name)


class Cookie(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    owner_name = models.CharField(_('Owner name'), max_length=50)
    url = models.URLField(_('URL'), unique=True)
    owner = models.ForeignKey(get_user_model(), verbose_name=_('User'),
                              on_delete=models.CASCADE)
    description = models.TextField(_('Description'), blank=True)
    license = models.CharField(_('License'), max_length=50, blank=True)
    last_change = models.DateTimeField(_('Last change'), null=True)
    last_poll = models.DateTimeField(_('Last poll'), null=True)
    backend = models.CharField(_('Backend'), max_length=25)
    mapping = JSONField(default={})

    # Hosting Statistics
    repo_watchers = models.IntegerField(_("repo watchers"), default=0)
    repo_forks = models.IntegerField(_("repo forks"), default=0)
    participants = models.TextField(_("Participants"),
        help_text="List of collaborats/participants on the project", blank=True)
    language = models.CharField(_('Language'), max_length=50, blank=True)
    homepage = models.CharField(_('Homepage'), max_length=255, blank=True)
    clone_urls = JSONField(default={})

    objects = CookieManager()

    class Meta:
        unique_together = ('name', 'owner_name')
        verbose_name = _('Cookie')
        verbose_name_plural = _('Cookies')

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return "{0}/{1}".format(self.owner_name, self.name)

    def fork(self, user):
        """
        :raises: ``UnknownObjectException`` is raised if the repository cannot
            be located.
        """
        fork = fork_repository(user, self.repository)
        cookie_dict = get_cookie_data_from_repo(fork)
        owner_dict = cookie_dict.pop('_owner', None)
        Cookie.objects.insert_from_cookie_dict(cookie_dict, owner_dict, self.repository)

    @property
    def repository(self):
        repository = getattr(self, '_repository', None)
        if not repository:
            repository = get_repo_from_full_name(self.full_name)
            setattr(self, '_repository', repository)
        return repository
