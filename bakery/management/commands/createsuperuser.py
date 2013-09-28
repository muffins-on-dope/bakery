# -*- coding: utf-8 -*-

import sys

from django.core.management.base import BaseCommand, CommandError

from bakery.auth.models import BakeryUser


class Command(BaseCommand):

    username = '<social-name>'
    help = 'Add a superuser with the given username. Login via the social API afterwards'

    def handle(self, username, *args, **options):
        traceback = options.get('traceback', False)
        try:
            BakeryUser.objects.create_superuser(username, None)
            self.stdout.write('Created {0}'.format(username))
        except ValueError as exc:
            ce = CommandError(exc)
            if traceback:
                tb = sys.exc_info()[2]
                raise ce.with_traceback(tb)
            else:
                raise ce
