# -*- coding: utf-8 -*-

from django.http import Http404


def detail(request, owner_name, name):
    raise Http404('{0}/{1}'.format(owner_name, name))
