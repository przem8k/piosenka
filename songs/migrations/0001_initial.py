# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import songs.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityContribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('performed', models.BooleanField(default=False, verbose_name='wyk.')),
                ('texted', models.BooleanField(default=False, verbose_name='tekst')),
                ('translated', models.BooleanField(default=False, verbose_name='tł.')),
                ('composed', models.BooleanField(default=False, verbose_name='muz.')),
                ('entity', models.ForeignKey(to='artists.Entity', verbose_name='artysta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, help_text='Tytuł piosenki.')),
                ('disambig', models.CharField(blank=True, max_length=100, null=True, help_text='Opcjonalna adnotacja rozróżniająca piosenki o tym samym tytule.')),
                ('original_title', models.CharField(blank=True, max_length=100, null=True, help_text="Tytuł oryginalnej piosenki w przypadku tłumaczenia, np. 'Mourir pour des idées'.")),
                ('link_youtube', models.URLField(blank=True, null=True, help_text='Link do nagrania piosenki w serwisie YouTube.')),
                ('link_wrzuta', models.URLField(blank=True, null=True, help_text='Link do nagrania piosenki w serwisie Wrzuta.')),
                ('score1', models.ImageField(blank=True, upload_to='scores', null=True)),
                ('score2', models.ImageField(blank=True, upload_to='scores', null=True)),
                ('score3', models.ImageField(blank=True, upload_to='scores', null=True)),
                ('capo_fret', models.IntegerField(validators=[songs.models.validate_capo_fret], default=0, help_text='Liczba od 0 do 11, 0 oznacza brak kapodastra.')),
                ('lyrics', models.TextField()),
                ('slug', models.SlugField(blank=True, unique=True, editable=False, max_length=100, help_text='Old slug, kept to maintain redirects.', null=True)),
                ('new_slug', models.SlugField(blank=True, unique=True, editable=False, max_length=200, help_text='Used in urls, has to be unique.', null=True)),
                ('published', models.BooleanField(default=True, editable=False, help_text='Unpublish instead of deleting.')),
                ('date', models.DateTimeField(editable=False)),
                ('has_extra_chords', models.BooleanField(default=False, editable=False, help_text='True iff the lyrics contain repeated chords.')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['title', 'disambig'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entitycontribution',
            name='song',
            field=models.ForeignKey(to='songs.Song'),
            preserve_default=True,
        ),
    ]
