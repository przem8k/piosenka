# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0003_auto_20160626_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='image_source',
        ),
        migrations.AddField(
            model_name='artist',
            name='image_author',
            field=models.CharField(null=True, max_length=50, help_text='Źródło zdjęcia (autor).', blank=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='image_url',
            field=models.URLField(null=True, help_text='Źródło zdjęcia (adres www).', blank=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='website',
            field=models.URLField(null=True, help_text='Strona internetowa artysty.', blank=True),
        ),
    ]
