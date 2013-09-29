# -*- coding: utf-8 -*-

from django.db.models import Q
from django.views.generic import ListView, TemplateView

from bakery.cookies.models import Cookie


class HomeView(ListView):
    model = Cookie
    template_name = 'home.html'

    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            q = Q(name__icontains=search_query) | Q(description__icontains=search_query)
            queryset = queryset.filter(q)
        return queryset

home = HomeView.as_view()


class StylesView(TemplateView):
    template_name = 'styles.html'

styles = StylesView.as_view()
