from django.contrib.auth import login as django_login
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from oauth.constants import SOCIAL_OAUTH_URLS
from oauth.social_oauth import GithubSocialOauth
from users.models import User
from utils.helpers import get_random_string


def index(request):
    return render(request, 'oauth/social.html', locals())


def social(request):
    provider = request.GET.get('provider', 'github')
    return HttpResponseRedirect(SOCIAL_OAUTH_URLS.get(provider))


def callback_github(request):
    code = request.GET.get('code', None)
    if not code:
        return HttpResponseRedirect('/error/?error=%s' % '缺少code参数')

    access_token, refresh_token = GithubSocialOauth.get_tokens(code)
    user_info = GithubSocialOauth.get_user_info(access_token)

    if 'message' in user_info:
        return HttpResponseRedirect('/error/?error=%s' % user_info['message'])

    print(user_info)

    user, is_create = User.objects.get_or_create(email=user_info['email'])
    if is_create:
        user.is_staff = False
        user.is_superuser = False
        user.username = user_info['name']
        user.avatar = user_info['avatar_url']
        user.set_password(get_random_string(10))
        user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    django_login(request, user)

    return HttpResponseRedirect('/')
