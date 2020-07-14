import uuid

from django.contrib.auth.models import Permission, User
from django.test import Client

_PASS = "secret"
_EMAIL = "example@example.com"
_NAME_LEN = 20


def create_user(perms=None):
    name = str(uuid.uuid4()).replace("-", "")[:_NAME_LEN]
    user = User.objects.create_user(username=name, email=_EMAIL, password=_PASS)

    if not perms:
        perms = []

    for perm in perms:
        parts = perm.split(".")
        assert len(parts) == 2
        permission = Permission.objects.get(
            content_type__app_label=parts[0], codename=parts[1]
        )
        user.user_permissions.add(permission)
    user.save()
    user.refresh_from_db()
    return user


def get_client(user=None):
    c = Client()
    if user:
        c.login(username=user.username, password=_PASS)
    return c


def get_user_client(user=None):
    if not user:
        user = create_user()
    return get_client(user=user)


def get_public_client():
    return get_client(user=None)
