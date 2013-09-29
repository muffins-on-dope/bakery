# -*- coding: utf-8 -*-

from django.db.models import Manager
from django.db.models.query import QuerySet

from bakery.auth.models import BakeryUser
from bakery.utils.vcs import gh


class ExtendedQuerySet(QuerySet):

    def update_or_create(self, *args, **kwargs):
        obj, created = self.get_or_create(*args, **kwargs)

        if not created:
            fields = dict(kwargs.pop("defaults", {}))
            fields.update(kwargs)
            for key, value in fields.items():
                setattr(obj, key, value)
            obj.save()

        return obj


class ExtendedManager(Manager):
    def get_query_set(self):
        return ExtendedQuerySet(self.model)

    def update_or_create(self, *args, **kwargs):
        return self.get_query_set().update_or_create(**kwargs)


class CookieManager(ExtendedManager):
    use_for_related_fields = True

    def import_from_url(self, url):
        """Imports or updates from ``url``"""
        if 'git@github.com' in url or 'https://github.com/' in url:
            repo = gh.get_repo_from_url(url)
            return self.import_from_repo(repo)

        raise ValueError('{0} is not a recognized URL'.format(url))

    def import_from_repo(self, repo):
        cookie_data = gh.get_cookie_data_from_repo(repo)
        owner_data = cookie_data.pop('_owner', None)
        return self.import_from_cookie_dict(cookie_data, owner_data, repo)

    def import_from_cookie_dict(self, cookie_dict, owner_dict, repo=None):
        username = owner_dict['username']
        email = owner_dict.get('email', None)

        if email is not None and not email.endswith('localhost.invalid'):
            filter_args = {'username': username, 'email': email}
        else:
            filter_args = {'username': username}

        filter_args['defaults'] = owner_dict

        owner, created = BakeryUser.objects.get_or_create(**filter_args)

        if created:
            owner.set_unusable_password()
            owner.save(update_fields=['password'])
        cookie_dict['owner'] = owner

        cookie = self.update_or_create(
            name=cookie_dict['name'],
            owner_name=cookie_dict['owner_name'],
            defaults=cookie_dict
        )
        if repo:
            setattr(cookie, '_repository', repo)
        return cookie
