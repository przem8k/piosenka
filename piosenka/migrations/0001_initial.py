# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import piosenka.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email_address', models.EmailField(max_length=254)),
                ('invitation_key', models.CharField(max_length=70, default=piosenka.models._get_default_invitation_key, editable=False)),
                ('expires_on', models.DateTimeField(default=piosenka.models._get_default_expires_on, editable=False)),
                ('is_valid', models.BooleanField(default=True, editable=False)),
                ('extended_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'permissions': [('invite', 'Can invite new contributors')],
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'permissions': [('inspect', 'Has access to debug views.')],
                'default_permissions': [],
            },
        ),
    ]
