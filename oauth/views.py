from django.contrib.auth import login as django_login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datetime_safe import datetime

from oauth.constants import SOCIAL_OAUTH_URLS
from oauth.social_oauth import GithubSocialOauth
from users.models import User


def index(request):
    title = '登陆'

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

    if not user_info['name']:
        username = user_info['login']
    else:
        username = user_info['name']

    if not user_info['email']:
        email = '%s@github.com' % user_info['login']
    else:
        email = user_info['email']

    try:
        user = User.objects.get(email=email)
        user.username = username
        user.github_username = user_info['login']
        user.avatar_url = user_info['avatar_url']
        user.last_login = datetime.now()
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(email=email,
                                        username=username,
                                        avatar=user_info['avatar_url'],
                                        github_username=user_info['login'])

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    django_login(request, user)

    return HttpResponseRedirect('/')
