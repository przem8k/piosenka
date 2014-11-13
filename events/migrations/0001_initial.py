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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.ForeignKey(to='artists.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text="Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego' lub 'V Festiwal Piosenki Wymyślnej w Katowicach'.", max_length=100)),
                ('datetime', models.DateTimeField()),
                ('description_trevor', models.TextField()),
                ('price', models.CharField(help_text='E.g. 20zł, wstęp wolny. W przypadku braku danych pozostaw puste.', null=True, max_length=100, blank=True)),
                ('website', models.URLField(help_text='Strona internetowa wydarzenia, źródło informacji. W przypadku braku danych pozostaw puste.', null=True, blank=True)),
                ('slug', models.SlugField(max_length=100, unique_for_date='datetime', editable=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(editable=False, default=True)),
                ('description_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datetime'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, editable=False, unique=True)),
                ('lat', models.FloatField(help_text='Latitude.', editable=False)),
                ('lon', models.FloatField(help_text='Longtitude.', editable=False)),
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
        migrations.AlterUniqueTogether(
            name='entityperformance',
            unique_together=set([('event', 'entity')]),
        ),
    ]
