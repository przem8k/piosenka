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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name for a band, lastname for a person.', max_length=50)),
                ('first_name', models.CharField(help_text='First (and possibly second) name if this is a person.', null=True, max_length=50, blank=True)),
                ('slug', models.SlugField(help_text='Used in urls, has to be unique.', max_length=100, unique=True)),
                ('featured', models.BooleanField(help_text='Iff true, it will be included in the songbook menu.', default=False)),
                ('still_plays', models.BooleanField(help_text='Iff true, the entity can be added on events.', default=False)),
                ('website', models.URLField(null=True, blank=True)),
                ('kind', models.IntegerField(choices=[(1, 'Wykonawca własnych tekstów'), (2, 'Kompozytor'), (3, 'Tłumacz'), (4, 'Wykonawca cudzych piosenek'), (5, 'Poeta nieśpiewający'), (6, 'Bard zagraniczny'), (7, 'Zespół')], help_text='Select the best fit.', null=True, blank=True)),
                ('is_band', models.BooleanField(help_text='Filled automaticely from type to facilitate sorting.', editable=False, default=False)),
            ],
            options={
                'ordering': ['is_band', 'name', 'first_name'],
            },
            bases=(models.Model,),
        ),
    ]
