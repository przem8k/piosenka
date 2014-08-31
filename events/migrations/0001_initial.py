# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('entity', models.ForeignKey(to='artists.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, help_text="Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego' lub 'V Festiwal Piosenki Wymyślnej w Katowicach'.")),
                ('datetime', models.DateTimeField()),
                ('description_trevor', models.TextField()),
                ('price', models.CharField(blank=True, max_length=100, null=True, help_text='E.g. 20zł, wstęp wolny. W przypadku braku danych pozostaw puste.')),
                ('website', models.URLField(blank=True, null=True, help_text='Strona internetowa wydarzenia, źródło informacji. W przypadku braku danych pozostaw puste.')),
                ('slug', models.SlugField(max_length=100, unique_for_date='datetime', editable=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(default=True, editable=False)),
                ('description_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['datetime'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True, editable=False)),
                ('lat', models.FloatField(editable=False, help_text='Latitude.')),
                ('lon', models.FloatField(editable=False, help_text='Longtitude.')),
            ],
            options={
                'ordering': ['town', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(to='events.Venue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entityperformance',
            name='event',
            field=models.ForeignKey(to='events.Event'),
            preserve_default=True,
        ),
    ]
