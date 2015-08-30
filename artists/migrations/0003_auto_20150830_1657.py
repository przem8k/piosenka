# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_auto_20150503_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='slug',
            field=models.SlugField(editable=False, unique=True, max_length=100),
        ),
    ]
