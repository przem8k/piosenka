# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0004_auto_20141206_0021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='new_slug',
            new_name='slug',
        ),
    ]
