# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piosenka', '0005_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permissions',
            options={'default_permissions': [], 'permissions': [('inspect', 'Has access to debug views.')]},
        ),
    ]
