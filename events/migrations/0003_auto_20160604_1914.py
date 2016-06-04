# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160604_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbevent',
            name='town',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
