# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20141221_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reviewed',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
