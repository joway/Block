from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate

from config.settings import JWT_AUTH
from users.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.username = 'joway'
        self.email = '670425438@qq.com'
        self.password = 'password'

        self.settings(JWT_AUTH=JWT_AUTH)

        self.user = User.objects.create_activate_user(username=self.username, email=self.email,
                                                      password=self.password)

    def auth_post(self, url, data=None):
        request = self.factory.post(url, data=data)
        force_authenticate(request, user=self.user)
        return request

    def auth_get(self, url, data=None):
        request = self.factory.get(url, data=data)
        force_authenticate(request, user=self.user)
        return request

    def get(self, url, data=None):
        request = self.factory.get(url, data=data)
        return request

    def post(self, url, data=None):
        request = self.factory.post(url, data=data)
        return request
