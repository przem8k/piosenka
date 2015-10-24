# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import content.slug


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityPerformance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('reviewed', models.BooleanField(editable=False, default=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('name', models.CharField(help_text="Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego'\nlub 'V Festiwal Piosenki Wymyślnej w Katowicach'.", max_length=100)),
                ('datetime', models.DateTimeField()),
                ('description_trevor', models.TextField()),
                ('price', models.CharField(blank=True, help_text='Np. 20zł, wstęp wolny. W przypadku braku danych pozostaw\npuste.', max_length=100, null=True)),
                ('website', models.URLField(blank=True, help_text='Strona internetowa wydarzenia, źródło informacji. W\nprzypadku braku danych pozostaw puste.', null=True)),
                ('slug', models.SlugField(editable=False, unique_for_date='datetime', max_length=100)),
                ('description_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': ['contribute'],
                'abstract': False,
                'ordering': ['datetime'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(editable=False, unique=True, max_length=100)),
                ('name', models.CharField(help_text='Imię i nazwisko wykonawcy lub nazwa zespołu.', max_length=50)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(editable=False, unique=True, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('lat', models.FloatField(editable=False, help_text='Latitude.', null=True)),
                ('lon', models.FloatField(editable=False, help_text='Longtitude.', null=True)),
            ],
            options={
                'ordering': ['town', 'name'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(to='events.Venue'),
        ),
        migrations.AddField(
            model_name='entityperformance',
            name='event',
            field=models.ForeignKey(to='events.Event'),
        ),
        migrations.AddField(
            model_name='entityperformance',
            name='performer',
            field=models.ForeignKey(to='events.Performer'),
        ),
    ]
