# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.http import require_POST

from bakery.cookies.models import Cookie


@login_required
@require_POST
def vote(request):
    cookie_id = int(request.POST.get('c'))
    try:
        cookie = Cookie.objects.get(pk=cookie_id)
        request.user.vote_for_cookie(cookie)
        redirect = reverse('cookies:detail', kwargs={
            'owner_name': cookie.owner_name,
            'name': cookie.name,
        })
        return HttpResponseRedirect(redirect)
    except Cookie.DoesNotExist:
        raise Http404('Cookie does not exist')
