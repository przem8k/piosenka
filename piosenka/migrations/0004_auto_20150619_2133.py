# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('piosenka', '0003_auto_20150619_2132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': [('invite', 'Can invite new contributors')]},
        ),
    ]
