# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import content.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='author',
            field=models.ForeignKey(default=content.models.get_default_author, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artist',
            name='pub_date',
            field=models.DateTimeField(default=content.models.get_default_pub_date, editable=False),
        ),
        migrations.AddField(
            model_name='artist',
            name='reviewed',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='author',
            field=models.ForeignKey(default=content.models.get_default_author, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='pub_date',
            field=models.DateTimeField(default=content.models.get_default_pub_date, editable=False),
        ),
        migrations.AlterField(
            model_name='song',
            name='author',
            field=models.ForeignKey(default=content.models.get_default_author, editable=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='song',
            name='pub_date',
            field=models.DateTimeField(default=content.models.get_default_pub_date, editable=False),
        ),
    ]
