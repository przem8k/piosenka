# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0002_auto_20141205_2342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='date',
            new_name='pub_date',
        ),
    ]
