# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_auto_20150830_1657'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Entity',
        ),
    ]
