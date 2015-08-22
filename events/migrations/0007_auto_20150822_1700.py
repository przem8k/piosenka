# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150503_1914'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'default_permissions': ['contribute'], 'ordering': ['datetime']},
        ),
    ]
