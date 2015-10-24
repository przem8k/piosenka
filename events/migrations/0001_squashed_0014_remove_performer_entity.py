# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import content.slug
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artists', '0001_squashed_0004_delete_entity'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityPerformance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.ForeignKey(to='artists.Entity')),
            ],
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
                ('slug', models.SlugField(unique_for_date='datetime', max_length=100, editable=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(default=True, editable=False)),
                ('description_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100, editable=False)),
                ('lat', models.FloatField(help_text='Latitude.', null=True, editable=False)),
                ('lon', models.FloatField(help_text='Longtitude.', null=True, editable=False)),
            ],
            options={
                'ordering': ['town', 'name'],
            },
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
        migrations.AlterUniqueTogether(
            name='entityperformance',
            unique_together=set([('event', 'entity')]),
        ),
        migrations.AddField(
            model_name='event',
            name='reviewed',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.RemoveField(
            model_name='event',
            name='published',
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(help_text="Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego'\nlub 'V Festiwal Piosenki Wymyślnej w Katowicach'.", max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.CharField(help_text='E.g. 20zł, wstęp wolny. W przypadku braku danych pozostaw\npuste.', null=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='website',
            field=models.URLField(help_text='Strona internetowa wydarzenia, źródło informacji. W\nprzypadku braku danych pozostaw puste.', null=True, blank=True),
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['datetime'], 'default_permissions': ['contribute']},
        ),
        migrations.CreateModel(
            name='Performer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, editable=False)),
                ('name', models.CharField(help_text='Imię i nazwisko wykonawcy lub nazwa zespołu.', max_length=50)),
                ('website', models.URLField(null=True, blank=True)),
                ('entity', models.ForeignKey(null=True, blank=True, to='artists.Entity')),
            ],
            options={
                'abstract': False,
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.CharField(help_text='Np. 20zł, wstęp wolny. W przypadku braku danych pozostaw\npuste.', null=True, max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='entityperformance',
            name='performer',
            field=models.ForeignKey(null=True, blank=True, to='events.Performer'),
        ),
        migrations.AlterField(
            model_name='entityperformance',
            name='entity',
            field=models.ForeignKey(null=True, blank=True, to='artists.Entity'),
        ),
        migrations.AlterUniqueTogether(
            name='entityperformance',
            unique_together=set([]),
        ),
        migrations.AlterField(
            model_name='entityperformance',
            name='performer',
            field=models.ForeignKey(default=1, to='events.Performer'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='performer',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='entityperformance',
            name='entity',
        ),
        migrations.RemoveField(
            model_name='performer',
            name='entity',
        ),
    ]
