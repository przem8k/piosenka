# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0012_auto_20150517_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='source_ref1',
            field=models.TextField(null=True, blank=True, help_text='Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na\npublikacjii.'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='source_ref2',
            field=models.TextField(null=True, blank=True, help_text='Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na\npublikacjii.'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='title',
            field=models.CharField(max_length=100, help_text='Tytuł adnotacji, np. "Aspazja" lub "Fortepian Chopina".'),
        ),
    ]
