import requests
from django.conf import settings
from django.utils.http import urlencode
from oauth.exceptions import SocialOauthProcessError, UserInfoError


class SocialBaseOauth(object):
    AUTH_URL = ''
    USER_URL = ''
    ACCESS_TOKEN_URL = ''
    PROVIDER = ''

    CLIENT_ID = ''
    CLIENT_SECRET = ''

    AUTH_DATA = {}

    UNIQUE_FIELD = 'id'

    HEADER = {"Accept": "application/json"}

    USERNAME_FIELD = 'username'

    @classmethod
    def get_token_data(cls, code):
        return {
            'code': code,
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'grant_type': "authorization_code"
        }

    @classmethod
    def get_tokens(cls, code):
        try:
            tokens = requests.get(url=cls.ACCESS_TOKEN_URL, params=cls.get_token_data(code=code),
                                  headers=cls.HEADER).json()
        except:
            raise SocialOauthProcessError
        access_token = tokens.get('access_token', None)
        refresh_token = tokens.get('refresh_token', None)
        return access_token, refresh_token

    @classmethod
    def get_user_info(cls, access_token):
        _data = {'access_token': access_token}
        try:
            info = requests.get(url=cls.USER_URL,
                                params=_data,
                                headers=cls.HEADER
                                ).json()
            return info
        except:
            raise SocialOauthProcessError

    @classmethod
    def get_auth_url(cls):
        return cls.AUTH_URL + '?' + urlencode(cls.AUTH_DATA)

    @classmethod
    def callback_url(cls):
        return settings.SOCIAL_CALLBACK_REDIRECT_BASE_URL + cls.PROVIDER

    @classmethod
    def get_provider(cls):
        return cls.PROVIDER

    @classmethod
    def get_unique_id(cls, access_token=None, info=None):
        if not info and access_token:
            info = cls.get_user_info(access_token=access_token)
        try:
            return info[cls.UNIQUE_FIELD]
        except:
            raise UserInfoError

    @classmethod
    def get_username(cls, access_token=None, info=None):
        if info and access_token is not None:
            info = cls.get_user_info(access_token=access_token)
        try:
            return info[cls.USERNAME_FIELD]
        except KeyError:
            raise UserInfoError


class GithubSocialOauth(SocialBaseOauth):
    PROVIDER = 'github'
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    USER_URL = 'https://api.github.com/user'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

    CLIENT_ID = settings.SOCIAL_AUTH_GITHUB_KEY
    CLIENT_SECRET = settings.SOCIAL_AUTH_GITHUB_SECRET

    UNIQUE_FIELD = 'email'
    USERNAME_FIELD = 'username'

    AUTH_DATA = {
        'client_id': settings.SOCIAL_AUTH_GITHUB_KEY,
        'redirect_uri': settings.GITHUB_SOCIAL_CALLBACK_REDIRECT_URL,
        'scope': 'user',
        'state': 'joway',
    }
