# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0013_auto_20150608_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annotation',
            options={'default_permissions': ['contribute']},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'default_permissions': ['contribute'], 'ordering': ['title', 'disambig']},
        ),
    ]
