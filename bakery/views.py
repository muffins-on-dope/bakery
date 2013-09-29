# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic import ListView, TemplateView, RedirectView
from django.contrib import auth

from bakery.cookies.models import Cookie
from bakery.socialize.models import Vote


class HomeView(ListView):
    model = Cookie
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user_votes = Vote.objects.get_for_user(self.request.user.id)
        voted_cookie_ids = user_votes.values_list('pk', flat=True).all()
        context['voted_cookie_ids'] = list(voted_cookie_ids)
        return context

home = HomeView.as_view()


class StylesView(TemplateView):
    template_name = 'styles.html'

styles = StylesView.as_view()


class LoginErrorView(TemplateView):
    template_name = 'error.html'

login_error = LoginErrorView.as_view()


class LogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        auth.logout(self.request)
        return reverse('home')

logout = LogoutView.as_view()
