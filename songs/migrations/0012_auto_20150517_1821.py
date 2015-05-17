# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0011_auto_20150517_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(default='error', editable=False, help_text='Used in urls, has to be unique.', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
