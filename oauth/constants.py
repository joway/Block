from .social_oauth import GithubSocialOauth


class Providers:
    Github = 1
    QQ = 2
    Coding = 3


PROVIDERS_CHOICES = (
    (Providers.Github, "Github"),
    (Providers.QQ, "QQ"),
    (Providers.Coding, "Coding"),
)

SOCIAL_OAUTH_URLS = {
    'github': GithubSocialOauth.get_auth_url(),
}
