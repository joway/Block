from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from oauth.exceptions import SocialOauthHasBound, SocialOauthNotExist
from oauth.models import SocialAccount
from oauth.services import SocialOauthService
from oauth.social_oauth import GithubSocialOauth
from utils.jwt import get_jwt_token
from utils.permissions import check_permission
from .constants import SOCIAL_OAUTH_URLS
from .serializers import SocialProviderSerializer, SocialCallbackSerializer, SocialAuthSerializer, \
    SocialAccountSerializer


class SocialAuthViewSet(viewsets.GenericViewSet):
    serializer_class = SocialCallbackSerializer
    queryset = SocialAccount.objects.all()
    permission_classes = [AllowAny, ]

    def list(self, request, *args, **kwargs):
        """
        展示用户名下的 所有 Social Oauth 信息
        """
        check_permission((IsAuthenticated,), self=self, request=request)
        socials = self.queryset.filter(user=request.user)
        return Response(data={SocialAccountSerializer(socials, many=True)}, status=status.HTTP_200_OK)

    @list_route(methods=['post'])
    def login(self, request):
        serializer = SocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = SocialOauthService.login(code=serializer.data['code'],
                                            provider=serializer.data['provider'])
            return Response(data={'token': get_jwt_token(user)}, status=status.HTTP_200_OK)
        except SocialOauthNotExist:
            return Response(data={'message': '该帐户未绑定'}, status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['get'])
    def redirect(self, request):
        """
        param provider
        重定向到授权界面
        """
        serializer = SocialProviderSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        return HttpResponseRedirect(SOCIAL_OAUTH_URLS.get(serializer.data['provider']))

    @list_route(methods=['post'])
    def binding(self, request):
        check_permission((IsAuthenticated,), self=self, request=request)
        serializer = SocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            SocialOauthService.binding(request.user, serializer.data['provider']
                                       , serializer.data['code'])
            return Response(data={'message': '绑定成功'}, status=status.HTTP_200_OK)
        except SocialOauthHasBound:
            return Response(data={'message': '社交帐号已被其它帐号绑定'}, status=status.HTTP_403_FORBIDDEN)

    @list_route(methods=['get'])
    def github(self, request):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        access_token = GithubSocialOauth.get_tokens(serializer.data['code'])
        user_info = GithubSocialOauth.get_user_info(access_token=access_token)
        if True:
            return Response(data={'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': '帐号未绑定, 跳转到登陆/注册界面'}, status=status.HTTP_403_FORBIDDEN)
