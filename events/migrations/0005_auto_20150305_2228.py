# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20141221_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='published',
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, help_text="Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego'\nlub 'V Festiwal Piosenki Wymyślnej w Katowicach'."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.CharField(max_length=100, help_text='E.g. 20zł, wstęp wolny. W przypadku braku danych pozostaw\npuste.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='website',
            field=models.URLField(help_text='Strona internetowa wydarzenia, źródło informacji. W\nprzypadku braku danych pozostaw puste.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
