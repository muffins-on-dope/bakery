# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from github import Github, GithubException

from bakery.cookies.models import Cookie
from bakery.utils.vcs.gh import fork_repository


def detail(request, owner_name, name):
    raise Http404('{0}/{1}'.format(owner_name, name))


@login_required
@require_POST
def fork(request, owner_name, name):
    cookie = get_object_or_404(Cookie, owner_name=owner_name, name=name)
    social_auth = request.user.social_auth.filter(provider=cookie.backend).all()
    if social_auth:
        social_auth = social_auth[0]
        try:
            github_api = Github(social_auth.extra_data['access_token'])
            gh_user = github_api.get_user()
            fork_repo = fork_repository(gh_user, cookie.repository)
            fork_cookie = Cookie.objects.import_from_repo(fork_repo)
            messages.success(
                request,
                _('Successfully forked %(name)s from %(parent_owner_name)s') % {
                    'parent_owner_name': cookie.owner_name,
                    'name': fork_cookie.name,
                }
            )

            redirect = reverse('cookies:detail', kwargs={
                'owner_name': fork_cookie.owner_name,
                'name': fork_cookie.name,
            })
        except GithubException as exc:
            message = exc.data.get('message', None) or str(exc.data)
            messages.error(
                request,
                _('An error occured while processing your request: %(status)d: %(message)s') % {
                    'status': exc.status,
                    'message': message,
                }
            )
            redirect = reverse('cookies:detail', kwargs={
                'owner_name': cookie.owner_name,
                'name': cookie.name,
            })

    else:
        messages.error(
            request,
            _('You don\'t have a account at %(provider)s assigned to your account') % {
                'provider': cookie.backend,
            }
        )
        redirect = reverse('cookies:detail', kwargs={
            'owner_name': cookie.owner_name,
            'name': cookie.name,
        })

    return HttpResponseRedirect(redirect)
