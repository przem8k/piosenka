# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-28 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0011_auto_20180719_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='artist_for_slug',
            field=models.CharField(blank=True, editable=False, max_length=100),
        ),
    ]