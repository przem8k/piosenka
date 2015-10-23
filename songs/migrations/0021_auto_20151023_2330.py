# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0020_auto_20151023_2316'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entitycontribution',
            unique_together=set([('song', 'artist')]),
        ),
    ]
