# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50, help_text='Name for a band, lastname for a person.')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, help_text='First (and possibly second) name if this is a person.')),
                ('slug', models.SlugField(max_length=100, unique=True, help_text='Used in urls, has to be unique.')),
                ('featured', models.BooleanField(default=False, help_text='Iff true, it will be included in the songbook menu.')),
                ('still_plays', models.BooleanField(default=False, help_text='Iff true, the entity can be added on events.')),
                ('website', models.URLField(blank=True, null=True)),
                ('kind', models.IntegerField(blank=True, help_text='Select the best fit.', null=True, choices=[(1, 'Wykonawca własnych tekstów'), (2, 'Kompozytor'), (3, 'Tłumacz'), (4, 'Wykonawca cudzych piosenek'), (5, 'Poeta nieśpiewający'), (6, 'Bard zagraniczny'), (7, 'Zespół')])),
                ('is_band', models.BooleanField(default=False, editable=False, help_text='Filled automaticely from type to facilitate sorting.')),
            ],
            options={
                'ordering': ['is_band', 'name', 'first_name'],
            },
            bases=(models.Model,),
        ),
    ]
