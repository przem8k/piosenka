# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0019_auto_20151023_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitycontribution',
            name='artist',
            field=models.ForeignKey(to='songs.Artist', default=0, verbose_name='artysta'),
            preserve_default=False,
        ),
    ]
