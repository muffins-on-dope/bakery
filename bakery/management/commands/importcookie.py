# -*- coding: utf-8 -*-

import sys

from django.core.management.base import BaseCommand, CommandError

from bakery.cookies.models import Cookie


class Command(BaseCommand):

    url = '<url>'
    help = 'Add the cookie defined by the VCS URL to the database.'

    def handle(self, url, *args, **options):
        verbosity = int(options.get('verbosity', 1))
        traceback = options.get('traceback', False)
        if verbosity > 1:
            self.stdout.write('Importing {0}'.format(url))
        try:
            Cookie.objects.import_from_url(url)
        except ValueError as exc:
            ce = CommandError(str(exc).format(url))
            if traceback:
                tb = sys.exc_info()[2]
                raise ce.with_traceback(tb)
            else:
                raise ce
