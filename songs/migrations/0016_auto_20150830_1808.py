# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0015_auto_20150830_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='core_slug',
            new_name='old_slug',
        ),
    ]
