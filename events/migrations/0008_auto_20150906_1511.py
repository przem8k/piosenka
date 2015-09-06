# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import content.slug


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_auto_20150830_1657'),
        ('events', '0007_auto_20150822_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('slug', models.SlugField(editable=False, unique=True, max_length=100)),
                ('name', models.CharField(max_length=50, help_text='Imię i nazwisko wykonawcy lub nazwa zespołu.')),
                ('website', models.URLField(null=True, blank=True)),
                ('entity', models.ForeignKey(to='artists.Entity', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.CharField(null=True, max_length=100, help_text='Np. 20zł, wstęp wolny. W przypadku braku danych pozostaw\npuste.', blank=True),
        ),
        migrations.AddField(
            model_name='entityperformance',
            name='performer',
            field=models.ForeignKey(to='events.Performer', null=True, blank=True),
        ),
    ]
