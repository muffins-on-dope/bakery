# -*- coding: utf-8 -*-

from django.contrib.auth.models import BaseUserManager

class BakeryUserManager(BaseUserManager):

    def _create_user(self, username, password, email, name, is_staff,
            is_organization, profile_url, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('No username given')
        if email:
            email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            name=name,
            is_staff=is_staff,
            is_active=True,
            is_organization=is_organization,
            profile_url=profile_url,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, None, None, False,
            **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, None, None, True,
            **extra_fields)
