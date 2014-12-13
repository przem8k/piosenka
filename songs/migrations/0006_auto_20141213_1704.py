# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0005_auto_20141207_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='ready',
            field=models.BooleanField(editable=False, default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='reviewed',
            field=models.BooleanField(editable=False, default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='core_slug',
            field=models.SlugField(unique=True, null=True, help_text='Old slug, kept to avoid duplicates and maintain redirects.', max_length=100, blank=True, editable=False),
            preserve_default=True,
        ),
    ]
