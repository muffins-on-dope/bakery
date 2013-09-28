# -*- coding: utf-8 -*-

from django.db.models import Manager

from bakery.utils.vcs import gh


class CookieManager(Manager):
    use_for_related_fields = True

    def import_from_url(self, url):
        if 'git@github.com' in url or 'https://github.com/' in url:
            repo = gh.get_repo_from_url(url)
            cookie_data = gh.get_cookie_data_from_repo(repo)
        else:
            raise ValueError('{0} is not a recognized URL')

        cookie = self.model(**cookie_data)
        cookie.save()
        return cookie
