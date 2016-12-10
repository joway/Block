from social.backends.github import GithubOAuth2


def get_avatar_url(request, backend, response, *args, **kwargs):
    """Pipeline to get user avatar from Twitter/FB via django-social-auth"""
    avatar_url = ''
    if isinstance(backend, GithubOAuth2):
        print(response)
        avatar_url = ''
    request.session['avatar_url'] = avatar_url
    return
