import uuid

from django.contrib.auth.models import User
from django.test import Client, TestCase

PASS = "secret"
EMAIL = "example@example.com"
NAME_LEN = 20


class UrlTestCase(TestCase):
    """ Creates two non-staff users:
     - user_alice
     - user_bob
     and two staff users:
     - user_approver_zoe
     - user_approver_jake
    """
    def get(self, url, user=None):
        return self.get_client(user).get(url)

    def get_client(self, user=None):
        c = Client()
        if user:
            c.login(username=user.username, password=PASS)
        return c

    def create_user_for_testing(self):
        name = str(uuid.uuid4()).replace("-", "")[:NAME_LEN]
        return User.objects.create_user(username=name,
                                        email=EMAIL,
                                        password=PASS)

    def setUp(self):
        super().setUp()
        self.user_alice = self.create_user_for_testing()
        self.user_bob = self.create_user_for_testing()
        self.user_approver_zoe = self.create_user_for_testing()
        self.user_approver_zoe.is_staff = True
        self.user_approver_zoe.save()
        self.user_approver_jake = self.create_user_for_testing()
        self.user_approver_jake.is_staff = True
        self.user_approver_jake.save()
