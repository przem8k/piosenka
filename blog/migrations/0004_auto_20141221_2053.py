# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141213_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='ready',
        ),
        migrations.AlterField(
            model_name='post',
            name='reviewed',
            field=models.BooleanField(editable=False, default=True),
            preserve_default=True,
        ),
    ]
