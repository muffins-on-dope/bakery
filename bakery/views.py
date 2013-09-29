# -*- coding: utf-8 -*-
from django.views.generic import ListView, TemplateView

from bakery.cookies.models import Cookie
from bakery.socialize.models import Vote


class HomeView(ListView):
    model = Cookie
    template_name = 'home.html'


home = HomeView.as_view()


class StylesView(TemplateView):
    template_name = 'styles.html'

styles = StylesView.as_view()
