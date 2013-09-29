# -*- coding: utf-8 -*-
from django.views.generic import ListView, TemplateView

from bakery.cookies.models import Cookie
from bakery.socialize.models import Vote


class HomeView(ListView):
    model = Cookie
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user_votes = Vote.objects.get_for_user(self.request.user.id)
        voted_cookie_ids = user_votes.values_list('cookie_id', flat=True).all()
        context['voted_cookie_ids'] = voted_cookie_ids
        return context

home = HomeView.as_view()


class StylesView(TemplateView):
    template_name = 'styles.html'

styles = StylesView.as_view()
