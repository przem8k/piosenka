# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import content.slug
import songs.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('reviewed', models.BooleanField(editable=False, default=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('title', models.CharField(help_text='Tytuł adnotacji, np. "Aspazja" lub "Fortepian Chopina".', max_length=100)),
                ('text_trevor', models.TextField()),
                ('image', models.ImageField(help_text='Ilustracja adnotacji. Pamiętaj o wskazaniu źródła tak samo jak w przypadku\ntreści zawartych w tekście adnotacji.', upload_to='song_annotations', null=True, blank=True)),
                ('source_url1', models.URLField(help_text='Link do źródła informacji, jeśli źródłem jest strona internetowa.', null=True, blank=True)),
                ('source_url2', models.URLField(help_text='Link do źródła informacji, jeśli źródłem jest strona internetowa.', null=True, blank=True)),
                ('source_ref1', models.TextField(help_text='Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na\npublikacjii.', null=True, blank=True)),
                ('source_ref2', models.TextField(help_text='Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na\npublikacjii.', null=True, blank=True)),
                ('slug', models.SlugField(help_text='Used in urls, has to be unique.', max_length=200, editable=False, unique=True)),
                ('text_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['contribute'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('slug', models.SlugField(editable=False, max_length=100, unique=True)),
                ('name', models.CharField(help_text='Imię i nazwisko wykonawcy lub nazwa zespołu.', max_length=50)),
                ('featured', models.BooleanField(help_text='Czy artysta powinien być wyświetlany w spisie treści\nśpiewnika.', default=False)),
                ('category', models.IntegerField(help_text='W której części spisu treści artysta ma być wyświetlony.\n', null=True, choices=[(1, 'Wykonawca własnych tekstów'), (2, 'Kompozytor'), (3, 'Bard zagraniczny'), (4, 'Zespół')], blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EntityContribution',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('performed', models.BooleanField(default=False, verbose_name='wyk.')),
                ('texted', models.BooleanField(default=False, verbose_name='tekst')),
                ('translated', models.BooleanField(default=False, verbose_name='tł.')),
                ('composed', models.BooleanField(default=False, verbose_name='muz.')),
                ('artist', models.ForeignKey(verbose_name='artysta', to='songs.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('reviewed', models.BooleanField(editable=False, default=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('title', models.CharField(help_text='Tytuł piosenki.', max_length=100)),
                ('disambig', models.CharField(help_text='Opcjonalna adnotacja rozróżniająca piosenki o tym samym tytule.', max_length=100, null=True, blank=True)),
                ('original_title', models.CharField(help_text="Tytuł oryginalnej piosenki w przypadku tłumaczenia, np. 'Mourir pour des idées'.", max_length=100, null=True, blank=True)),
                ('link_youtube', models.URLField(help_text='Link do nagrania piosenki w serwisie YouTube.', null=True, blank=True)),
                ('link_wrzuta', models.URLField(help_text='Link do nagrania piosenki w serwisie Wrzuta.', null=True, blank=True)),
                ('score1', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('score2', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('score3', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('capo_fret', models.IntegerField(validators=[songs.models.validate_capo_fret], help_text='Liczba od 0 do 11, 0 oznacza brak kapodastra.', default=0)),
                ('lyrics', models.TextField()),
                ('old_slug', models.SlugField(help_text='Old slug kept to maintain redirects.', editable=False, null=True, blank=True, max_length=100, unique=True)),
                ('slug', models.SlugField(help_text='Used in urls, has to be unique.', max_length=200, editable=False, unique=True)),
                ('has_extra_chords', models.BooleanField(help_text='True iff the lyrics contain repeated chords.', editable=False, default=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['title', 'disambig'],
                'default_permissions': ['contribute'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.AddField(
            model_name='entitycontribution',
            name='song',
            field=models.ForeignKey(to='songs.Song'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='song',
            field=models.ForeignKey(editable=False, to='songs.Song'),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('title', 'disambig')]),
        ),
        migrations.AlterUniqueTogether(
            name='entitycontribution',
            unique_together=set([('song', 'artist')]),
        ),
    ]
