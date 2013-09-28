# -*- coding: utf-8 -*-
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm


class IndexView(TemplateView):
    template_name = 'index.html'

index = IndexView.as_view()


class LoginErrorView(TemplateView):
    template_name = 'error.html'

login_error = LoginErrorView.as_view()
