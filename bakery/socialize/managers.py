# -*- coding: utf-8 -*-

from django.db.models import Manager
from django.db.models.query import QuerySet


class VoteQuerySet(QuerySet):

    def get_for_cookie(self, cookie):
        return self.filter(cookie=cookie)

    def get_for_user(self, user):
        return self.filter(user=user)

    def get_for_user_and_cookie(self, user, cookie):
        return self.filter(user=user, cookie=cookie)

    def has_voted(self, user, cookie):
        return self.get_for_user_and_cookie(user, cookie).count() == 1


class VoteManager(Manager):

    use_for_related_fields = True

    def get_query_set(self):
        return VoteQuerySet(self.model)

    def get_for_cookie(self, cookie):
        return self.get_query_set().get_for_cookie(cookie)

    def get_for_user(self, user):
        return self.get_query_set().get_for_user(user)

    def get_for_user_and_cookie(self, user, cookie):
        return self.get_query_set().get_for_user_and_cookie(user, cookie)

    def has_voted(self, user, cookie):
        return self.get_query_set().has_voted(user, cookie)
