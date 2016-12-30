from django.test import TestCase
from rest_framework.test import APIRequestFactory

from users.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.username = 'joway'
        self.email = '670425438@qq.com'
        self.password = 'password'
        self.user = User.objects.create_activate_user(username=self.username, email=self.email,
                                                      password=self.password)
