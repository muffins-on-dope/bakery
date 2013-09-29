# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from bakery.auth.models import BakeryUser
from bakery.cookies.models import Cookie
from bakery.socialize.models import do_vote, do_unvote


@login_required
@require_POST
def vote(request, unvote=False):
    cookie_id = int(request.POST.get('c'))
    try:
        cookie = Cookie.objects.get(pk=cookie_id)
        if unvote:
            do_unvote(request.user, cookie)
        else:
            do_vote(request.user, cookie)
        redirect = reverse('cookies:detail', kwargs={
            'owner_name': cookie.owner_name,
            'name': cookie.name,
        })
        return HttpResponseRedirect(redirect)
    except Cookie.DoesNotExist:
        raise Http404('Cookie does not exist')


class VotesView(DetailView):
    model = Cookie
    template_name = 'socialize/votes.html'

    def get_context_data(self, **kwargs):
        context = super(VotesView, self).get_context_data(**kwargs)
        context['users'] = self.object.votes.all()
        return context

votes_for_cookie = VotesView.as_view()


class VotedView(DetailView):
    model = BakeryUser
    template_name = 'socialize/voted.html'

    def get_context_data(self, **kwargs):
        context = super(VotedView, self).get_context_data(**kwargs)
        context['cookies'] = self.object.votes.all()
        return context

votes_by_user = VotedView.as_view()
