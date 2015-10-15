# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_remove_entityperformance_entity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performer',
            name='entity',
        ),
    ]
