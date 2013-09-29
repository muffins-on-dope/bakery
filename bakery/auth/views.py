from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView
from django.contrib import auth

from bakery.auth.models import BakeryUser


class LoginErrorView(TemplateView):
    template_name = 'error.html'

login_error = LoginErrorView.as_view()


class LogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        auth.logout(self.request)
        return reverse('home')

logout = LogoutView.as_view()


class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = BakeryUser.objects.get(username=kwargs['username'])
        context['bakery_user'] = user
        return context

profile = ProfileView.as_view()
