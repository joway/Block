from django.conf import settings
from django.db import models


# Create your models here.
from oauth.constants import PROVIDERS_CHOICES


class SocialAccount(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='绑定帐户')
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField('refresh_token', max_length=255, blank=True, null=True)

    provider = models.IntegerField('类别', choices=PROVIDERS_CHOICES, max_length=10)
    bound_at = models.DateTimeField('绑定时间', auto_now_add=True)
    expire_at = models.DateTimeField('token失效时间', blank=True, null=True)
