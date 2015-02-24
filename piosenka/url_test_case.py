import uuid

from django.contrib.auth.models import User
from django.test import Client, TestCase

PASS = "secret"
EMAIL = "example@example.com"
NAME_LEN = 20


class UrlTestCase(TestCase):
    def get(self, url, user=None):
        c = Client()
        if user:
            c.login(username=user.username, password=PASS)
        return c.get(url)

    def create_user_for_testing(self):
        name = str(uuid.uuid4()).replace("-", "")[:NAME_LEN]
        return User.objects.create_user(username=name,
                                        email=EMAIL,
                                        password=PASS)

    def setUp(self):
        super().setUp()
        self.user_alice = self.create_user_for_testing()
        self.user_bob = self.create_user_for_testing()
        self.user_approver = self.create_user_for_testing()
        self.user_approver.is_staff = True
        self.user_approver.save()
