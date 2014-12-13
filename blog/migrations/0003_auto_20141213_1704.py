# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20141205_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ready',
            field=models.BooleanField(editable=False, default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='reviewed',
            field=models.BooleanField(editable=False, default=False),
            preserve_default=True,
        ),
    ]
