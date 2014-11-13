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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('performed', models.BooleanField(verbose_name='wyk.', default=False)),
                ('texted', models.BooleanField(verbose_name='tekst', default=False)),
                ('translated', models.BooleanField(verbose_name='tł.', default=False)),
                ('composed', models.BooleanField(verbose_name='muz.', default=False)),
                ('entity', models.ForeignKey(verbose_name='artysta', to='artists.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Tytuł piosenki.', max_length=100)),
                ('disambig', models.CharField(help_text='Opcjonalna adnotacja rozróżniająca piosenki o tym samym tytule.', null=True, max_length=100, blank=True)),
                ('original_title', models.CharField(help_text="Tytuł oryginalnej piosenki w przypadku tłumaczenia, np. 'Mourir pour des idées'.", null=True, max_length=100, blank=True)),
                ('link_youtube', models.URLField(help_text='Link do nagrania piosenki w serwisie YouTube.', null=True, blank=True)),
                ('link_wrzuta', models.URLField(help_text='Link do nagrania piosenki w serwisie Wrzuta.', null=True, blank=True)),
                ('score1', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('score2', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('score3', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('capo_fret', models.IntegerField(validators=[songs.models.validate_capo_fret], help_text='Liczba od 0 do 11, 0 oznacza brak kapodastra.', default=0)),
                ('lyrics', models.TextField()),
                ('slug', models.SlugField(help_text='Old, core slug, kept to avoid duplicates and maintain redirects.', editable=False, unique=True, null=True, blank=True, max_length=100)),
                ('new_slug', models.SlugField(help_text='Used in urls, has to be unique.', editable=False, unique=True, null=True, blank=True, max_length=200)),
                ('published', models.BooleanField(help_text='Unpublish instead of deleting.', editable=False, default=True)),
                ('date', models.DateTimeField(editable=False)),
                ('has_extra_chords', models.BooleanField(help_text='True iff the lyrics contain repeated chords.', editable=False, default=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
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
