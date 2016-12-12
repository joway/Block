from django.contrib.auth import login as django_login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from oauth.constants import SOCIAL_OAUTH_URLS
from oauth.social_oauth import GithubSocialOauth
from users.models import User


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

    try:
        user = User.objects.get(email=user_info['email'])
    except User.DoesNotExist:
        user = User.objects.create_user(email=user_info['email'], username=user_info['name'], avatar=user_info['avatar_url'])

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    django_login(request, user)

    return HttpResponseRedirect('/')
