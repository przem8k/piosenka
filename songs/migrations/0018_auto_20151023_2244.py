# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0017_auto_20151023_2229'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entitycontribution',
            unique_together=set([]),
        ),
    ]
