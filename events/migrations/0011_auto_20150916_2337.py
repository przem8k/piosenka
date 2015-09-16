# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150914_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entityperformance',
            name='performer',
            field=models.ForeignKey(default=1, to='events.Performer'),
            preserve_default=False,
        ),
    ]
