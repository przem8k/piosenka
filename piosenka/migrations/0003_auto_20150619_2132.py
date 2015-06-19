# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piosenka', '0002_auto_20150619_2129'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': [('invite', 'Invite')]},
        ),
    ]
