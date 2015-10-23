# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0018_auto_20151023_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitycontribution',
            name='entity',
            field=models.ForeignKey(null=True, to='artists.Entity', verbose_name='artysta', blank=True),
        ),
    ]
