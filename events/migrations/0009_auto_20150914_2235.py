# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150906_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entityperformance',
            name='entity',
            field=models.ForeignKey(null=True, blank=True, to='artists.Entity'),
        ),
    ]
