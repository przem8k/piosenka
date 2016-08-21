# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import content.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160604_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entityperformance',
            name='event',
        ),
        migrations.RemoveField(
            model_name='entityperformance',
            name='performer',
        ),
        migrations.AlterField(
            model_name='event',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=content.models.get_default_author, editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_date',
            field=models.DateTimeField(editable=False, default=content.models.get_default_pub_date),
        ),
        migrations.DeleteModel(
            name='EntityPerformance',
        ),
    ]
