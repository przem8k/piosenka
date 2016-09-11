# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-11 13:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0004_auto_20160719_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='pub_date',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='artist',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='artist',
            name='pub_date',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='song',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='song',
            name='pub_date',
            field=models.DateTimeField(editable=False),
        ),
    ]
