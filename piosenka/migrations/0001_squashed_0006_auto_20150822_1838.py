# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import piosenka.models
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('piosenka', '0001_initial'), ('piosenka', '0002_auto_20150619_2129'), ('piosenka', '0003_auto_20150619_2132'), ('piosenka', '0004_auto_20150619_2133'), ('piosenka', '0005_permissions'), ('piosenka', '0006_auto_20150822_1838')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('email_address', models.EmailField(max_length=254)),
                ('invitation_key', models.CharField(editable=False, max_length=70)),
                ('expires_on', models.DateTimeField(editable=False)),
                ('is_valid', models.BooleanField(editable=False, default=True)),
                ('extended_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': ('invite', 'Invite')},
        ),
        migrations.AlterField(
            model_name='invitation',
            name='expires_on',
            field=models.DateTimeField(editable=False, default=piosenka.models._get_default_expires_on),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='invitation_key',
            field=models.CharField(editable=False, default=piosenka.models._get_default_invitation_key, max_length=70),
        ),
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': [('invite', 'Invite')]},
        ),
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': [('invite', 'Can invite new contributors')]},
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
            ],
            options={
                'default_permissions': [],
                'permissions': [('debug', 'Has access to debug views.')],
            },
        ),
        migrations.AlterModelOptions(
            name='permissions',
            options={'default_permissions': [], 'permissions': [('inspect', 'Has access to debug views.')]},
        ),
    ]
