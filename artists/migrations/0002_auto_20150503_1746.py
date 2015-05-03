# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='slug',
            field=models.SlugField(max_length=100, help_text='Used in urls, has to be unique.', editable=False, unique=True),
        ),
    ]
