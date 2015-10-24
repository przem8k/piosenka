# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import content.slug
from django.conf import settings
import songs.models


class Migration(migrations.Migration):

    replaces = [('songs', '0001_initial'), ('songs', '0002_auto_20141205_2342'), ('songs', '0003_auto_20141205_2358'), ('songs', '0004_auto_20141206_0021'), ('songs', '0005_auto_20141207_1914'), ('songs', '0006_auto_20141213_1704'), ('songs', '0007_auto_20141221_2053'), ('songs', '0008_auto_20141221_2255'), ('songs', '0009_remove_song_published'), ('songs', '0010_annotation'), ('songs', '0011_auto_20150517_1724'), ('songs', '0012_auto_20150517_1821'), ('songs', '0013_auto_20150608_2105'), ('songs', '0014_auto_20150822_1700'), ('songs', '0015_auto_20150830_1637'), ('songs', '0016_auto_20150830_1808'), ('songs', '0017_auto_20151023_2229'), ('songs', '0018_auto_20151023_2244'), ('songs', '0019_auto_20151023_2253'), ('songs', '0020_auto_20151023_2316'), ('songs', '0021_auto_20151023_2330'), ('songs', '0022_auto_20151023_2335')]

    dependencies = [
        ('artists', '0001_squashed_0004_delete_entity'),
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
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='Tytuł piosenki.')),
                ('disambig', models.CharField(max_length=100, help_text='Opcjonalna adnotacja rozróżniająca piosenki o tym samym tytule.', null=True, blank=True)),
                ('original_title', models.CharField(max_length=100, help_text="Tytuł oryginalnej piosenki w przypadku tłumaczenia, np. 'Mourir pour des idées'.", null=True, blank=True)),
                ('link_youtube', models.URLField(help_text='Link do nagrania piosenki w serwisie YouTube.', null=True, blank=True)),
                ('link_wrzuta', models.URLField(help_text='Link do nagrania piosenki w serwisie Wrzuta.', null=True, blank=True)),
                ('score1', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('score2', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('score3', models.ImageField(upload_to='scores', null=True, blank=True)),
                ('capo_fret', models.IntegerField(default=0, help_text='Liczba od 0 do 11, 0 oznacza brak kapodastra.', validators=[songs.models.validate_capo_fret])),
                ('lyrics', models.TextField()),
                ('core_slug', models.SlugField(help_text='Old slug, kept to avoid duplicates and maintain redirects.', editable=False, max_length=100, unique=True, null=True, blank=True)),
                ('slug', models.SlugField(help_text='Used in urls, has to be unique.', editable=False, max_length=200, unique=True, null=True, blank=True)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('has_extra_chords', models.BooleanField(help_text='True iff the lyrics contain repeated chords.', default=False, editable=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'ordering': ['title', 'disambig'],
            },
        ),
        migrations.AddField(
            model_name='entitycontribution',
            name='song',
            field=models.ForeignKey(to='songs.Song'),
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=100, help_text='Tytuł adnotacji, np. "Aspazja" lub "Fortepian Chopina".')),
                ('text_trevor', models.TextField()),
                ('image', models.ImageField(help_text='Ilustracja adnotacji. Pamiętaj o wskazaniu źródła tak samo jak w przypadku\ntreści zawartych w tekście adnotacji.', upload_to='song_annotations', null=True, blank=True)),
                ('source_url1', models.URLField(help_text='Link do źródła informacji, jeśli źródłem jest strona internetowa.', null=True, blank=True)),
                ('source_url2', models.URLField(help_text='Link do źródła informacji, jeśli źródłem jest strona internetowa.', null=True, blank=True)),
                ('source_ref1', models.TextField(help_text='Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na\npublikacjii.', null=True, blank=True)),
                ('source_ref2', models.TextField(help_text='Tytuł i autor publikacji źródłowej, jeśli adnotacja jest oparta na\npublikacjii.', null=True, blank=True)),
                ('slug', models.SlugField(max_length=200, help_text='Used in urls, has to be unique.', unique=True, editable=False)),
                ('text_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(editable=False, to='songs.Song')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='entitycontribution',
            unique_together=set([('song', 'entity')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(help_text='Used in urls, has to be unique.', default='error', editable=False, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='annotation',
            options={'default_permissions': ['contribute']},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'default_permissions': ['contribute'], 'ordering': ['title', 'disambig']},
        ),
        migrations.AlterField(
            model_name='song',
            name='core_slug',
            field=models.SlugField(help_text='Old slug kept to maintain redirects.', editable=False, max_length=100, unique=True, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='song',
            unique_together=set([('title', 'disambig')]),
        ),
        migrations.RenameField(
            model_name='song',
            old_name='core_slug',
            new_name='old_slug',
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100, unique=True, editable=False)),
                ('name', models.CharField(max_length=50, help_text='Imię i nazwisko wykonawcy lub nazwa zespołu.')),
                ('featured', models.BooleanField(help_text='Czy artysta powinien być wyświetlany w spisie treści\nśpiewnika.', default=False)),
                ('category', models.IntegerField(help_text='W której części spisu treści artysta ma być wyświetlony.\n', blank=True, null=True, choices=[(1, 'Wykonawca własnych tekstów'), (2, 'Kompozytor'), (3, 'Bard zagraniczny'), (4, 'Zespół')])),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.AddField(
            model_name='entitycontribution',
            name='artist',
            field=models.ForeignKey(verbose_name='artysta (nowy)', to='songs.Artist', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='entitycontribution',
            unique_together=set([]),
        ),
        migrations.AlterField(
            model_name='entitycontribution',
            name='entity',
            field=models.ForeignKey(verbose_name='artysta', to='artists.Entity', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='entitycontribution',
            name='artist',
            field=models.ForeignKey(verbose_name='artysta', default=0, to='songs.Artist'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='entitycontribution',
            unique_together=set([('song', 'artist')]),
        ),
        migrations.RemoveField(
            model_name='entitycontribution',
            name='entity',
        ),
    ]
