# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141213_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='ready',
        ),
        migrations.AlterField(
            model_name='event',
            name='reviewed',
            field=models.BooleanField(editable=False, default=True),
            preserve_default=True,
        ),
    ]
