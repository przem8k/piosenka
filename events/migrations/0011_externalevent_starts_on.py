# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-11 14:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_delete_fbevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalevent',
            name='starts_on',
            field=models.DateField(default=datetime.date(2018, 8, 11), help_text='Data rozpoczęcia wydarzenia.', verbose_name='Dzień rozpoczęcia'),
            preserve_default=False,
        ),
    ]