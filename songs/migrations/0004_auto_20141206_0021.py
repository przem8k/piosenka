# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20141205_2358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='slug',
            new_name='core_slug',
        ),
    ]
