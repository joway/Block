from .constants import Providers
from .exceptions import SocialOauthNotExist, BindingProcessError, SocialOauthHasBound
from .models import SocialAccount
from .social_oauth import GithubSocialOauth


class SocialOauthService(object):
    @classmethod
    def get_social_oauth_agent(cls, provider):
        if provider == Providers.Github:
            return GithubSocialOauth
        else:
            raise BindingProcessError

    @classmethod
    def binding(cls, user, provider, code):
        Agent = cls.get_social_oauth_agent(provider)
        access_token, refresh_token = Agent.get_tokens(code)
        user_info = Agent.get_user_info(access_token=access_token)

        social_oauth, is_create = SocialAccount.objects.get_or_create(provider=provider,
                                                                      uid=Agent.get_unique_id(info=user_info))
        if not is_create:
            raise SocialOauthHasBound

        social_oauth.user = user
        social_oauth.access_token = access_token
        social_oauth.refresh_token = refresh_token
        social_oauth.username = Agent.get_username(info=user_info)
        social_oauth.save()
        return social_oauth

    @classmethod
    def disbinding(cls, user, provider):
        try:
            social_oauth = SocialAccount.objects.get(user=user, provider=provider)
        except SocialAccount.DoesNotExist:
            raise SocialOauthNotExist
        social_oauth.delete()

    @classmethod
    def login(cls, code, provider):
        Agent = cls.get_social_oauth_agent(provider)
        access_token, refresh_token = Agent.get_tokens(code)
        try:
            social_oauth = SocialAccount.objects.get(provider=provider,
                                                     uid=Agent.get_unique_id(access_token))
            return social_oauth.user
        except SocialAccount.DoesNotExist:
            raise SocialOauthNotExist

    @classmethod
    def refresh(cls):
        pass
