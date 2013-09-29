#-*- coding: utf-8 -*-
from bakery.socialize.models import Vote


def voted_cookies(request):
    user_votes = Vote.objects.get_for_user(request.user.id)
    voted_cookie_ids = user_votes.values_list('cookie_id', flat=True).all()
    return {'voted_cookie_ids': voted_cookie_ids}
