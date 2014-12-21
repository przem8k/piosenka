# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20141213_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='ready',
        ),
        migrations.AlterField(
            model_name='article',
            name='reviewed',
            field=models.BooleanField(editable=False, default=True),
            preserve_default=True,
        ),
    ]
