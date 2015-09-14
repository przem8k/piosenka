# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150914_2235'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entityperformance',
            unique_together=set([]),
        ),
    ]
