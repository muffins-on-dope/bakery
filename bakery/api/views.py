# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse


from bakery.cookies.models import Cookie


DUMPS_KWARGS = {
    'cls': DjangoJSONEncoder,
    'indent': True if settings.DEBUG else None
}


class JSONResponse(HttpResponse):

    def __init__(self, data):
        super(JSONResponse, self).__init__(
            json.dumps(data, **DUMPS_KWARGS),
            content_type='application/json'
        )


def cookies_list(request, page=1):
    page = int(page)
    if page < 1:
        page = 1
    per_page = settings.BAKERY_API_COOKIES_PER_PAGE
    start = (page-1) * per_page
    end =  page * per_page
    cookies = list(Cookie.objects.values('name', 'url', 'description', 'last_change').all()[start:end])
    return JSONResponse(cookies)


def cookies_search(request, term):
    q = Q(name__icontains=term) | Q(description__icontains=term)
    cookies = list(Cookie.objects.filter(q).values('name', 'url', 'description', 'last_change').all())
    return JSONResponse(cookies)
