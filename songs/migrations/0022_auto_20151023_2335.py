# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0021_auto_20151023_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='entitycontribution',
            name='entity',
        ),
    ]
