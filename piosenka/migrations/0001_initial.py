# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('email_address', models.EmailField(max_length=254)),
                ('invitation_key', models.CharField(max_length=70, editable=False)),
                ('expires_on', models.DateTimeField(editable=False)),
                ('is_valid', models.BooleanField(default=True, editable=False)),
                ('extended_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
        ),
    ]
