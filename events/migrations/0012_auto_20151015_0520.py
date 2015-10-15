# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150916_2337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performer',
            options={'ordering': ['name']},
        ),
    ]
