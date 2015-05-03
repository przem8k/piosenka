# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150305_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='lat',
            field=models.FloatField(help_text='Latitude.', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='venue',
            name='lon',
            field=models.FloatField(help_text='Longtitude.', null=True, editable=False),
        ),
    ]
