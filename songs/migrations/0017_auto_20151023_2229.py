# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import content.slug


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_auto_20150830_1657'),
        ('songs', '0016_auto_20150830_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('slug', models.SlugField(unique=True, editable=False, max_length=100)),
                ('name', models.CharField(max_length=50, help_text='Imię i nazwisko wykonawcy lub nazwa zespołu.')),
                ('featured', models.BooleanField(help_text='Czy artysta powinien być wyświetlany w spisie treści\nśpiewnika.', default=False)),
                ('category', models.IntegerField(choices=[(1, 'Wykonawca własnych tekstów'), (2, 'Kompozytor'), (3, 'Bard zagraniczny'), (4, 'Zespół')], null=True, blank=True, help_text='W której części spisu treści artysta ma być wyświetlony.\n')),
                ('website', models.URLField(null=True, blank=True)),
                ('entity', models.ForeignKey(to='artists.Entity', blank=True, null=True, help_text='temp')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
        migrations.AddField(
            model_name='entitycontribution',
            name='artist',
            field=models.ForeignKey(verbose_name='artysta (nowy)', to='songs.Artist', blank=True, null=True),
        ),
    ]
