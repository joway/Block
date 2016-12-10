# coding=utf-8


class SocialOauthExist(Exception):
    pass


class SocialOauthNotExist(Exception):
    pass


class SocialOauthProcessError(Exception):
    pass


class BindingProcessError(Exception):
    pass


class SocialOauthHasBound(Exception):
    pass


class UserInfoError(Exception):
    pass
