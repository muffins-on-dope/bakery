# -*- coding: utf-8 -*-

from django.db.models import Manager

from bakery.auth.models import BakeryUser
from bakery.utils.vcs import gh


class CookieManager(Manager):
    use_for_related_fields = True

    def import_from_url(self, url):
        if 'git@github.com' in url or 'https://github.com/' in url:
            repo = gh.get_repo_from_url(url)
            cookie_data = gh.get_cookie_data_from_repo(repo)
            owner_data = cookie_data.pop('_owner', None)
        else:
            raise ValueError('{0} is not a recognized URL')

        return self.insert_from_cookie_dict(cookie_data, owner_data, repo)

    def insert_from_cookie_dict(self, cookie_dict, owner_dict, repo=None):
        owner, created = BakeryUser.objects.get_or_create(**owner_dict)
        if created:
            owner.set_unusable_password()
            owner.save(update_fields=['password'])
        cookie_dict['owner'] = owner

        cookie = self.model(**cookie_dict)
        cookie.save()
        if repo:
            setattr(cookie, '_repository', repo)
        return cookie
