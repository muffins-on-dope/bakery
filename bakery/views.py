# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import auth

from bakery.cookies.models import Cookie


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        return {'cookies': Cookie.objects.all()}

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
