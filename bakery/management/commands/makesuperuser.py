# -*- coding: utf-8 -*-

import sys

from django.core.management.base import BaseCommand, CommandError

from bakery.auth.models import BakeryUser


class Command(BaseCommand):

    username = '<username>'
    help = 'Change the user <username> to be a superuser.'

    def handle(self, username, **options):
        traceback = options.get('traceback', False)
        try:
            user = BakeryUser.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.save(update_fields=['is_staff', 'is_superuser'])
            self.stdout.write('Updated {0} to superuser status'.format(username))
        except (BakeryUser.DoesNotExist, ValueError) as exc:
            ce = CommandError(exc)
            if traceback:
                tb = sys.exc_info()[2]
                raise ce.with_traceback(tb)
            else:
                raise ce
