# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20151015_0520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entityperformance',
            name='entity',
        ),
    ]
