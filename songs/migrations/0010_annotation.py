# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songs', '0009_remove_song_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('reviewed', models.BooleanField(editable=False, default=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('title', models.CharField(help_text='Tytuł adnotacji, np. "Aspazja", "Francuska choroba", "Rok 1788". Adnotacje\npoświęcone dziełom artystycznym tytułuj wg schematu "Nazwa - Autor", np.\n"Fortepian Chopina - Cyprian Kamil Norwid" lub "Wojna postu z karnawałem - Piotr\nBreugel.', max_length=100)),
                ('text_trevor', models.TextField()),
                ('image', models.ImageField(help_text='Ilustracja adnotacji. Pamiętaj o wskazaniu źródła tak samo jak w przypadku\ntreści zawartych w tekście adnotacji.', blank=True, upload_to='song_annotations', null=True)),
                ('source_url1', models.URLField(help_text='Link do źródła informacji, jeśli źródłem jest strona internetowa.', blank=True, null=True)),
                ('source_url2', models.URLField(help_text='Link do źródła informacji, jeśli źródłem jest strona internetowa.', blank=True, null=True)),
                ('source_ref1', models.TextField(help_text='Nazwa publikacji źródłowej, jeśli adnotacja jest oparta na publikacjii.', blank=True, null=True)),
                ('source_ref2', models.TextField(help_text='Nazwa publikacji źródłowej, jeśli adnotacja jest oparta na publikacjii.', blank=True, null=True)),
                ('slug', models.SlugField(editable=False, unique=True, max_length=200, help_text='Used in urls, has to be unique.')),
                ('text_html', models.TextField(editable=False)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
                ('song', models.ForeignKey(editable=False, to='songs.Song')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
