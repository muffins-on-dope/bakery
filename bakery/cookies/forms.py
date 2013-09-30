#-*- coding: utf-8 -*-
from django import forms
from bakery.cookies.models import Cookie


class ImportForm(forms.Form):
    url = forms.CharField(max_length=255)

    def import_cookie(self):
        url = self.cleaned_data['url']
        cookie = Cookie.objects.import_from_url(url)
        return cookie
