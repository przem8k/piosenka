# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0014_auto_20150822_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='core_slug',
            field=models.SlugField(max_length=100, blank=True, null=True, unique=True, help_text='Old slug kept to maintain redirects.', editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('title', 'disambig')]),
        ),
    ]
