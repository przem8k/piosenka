# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0002_auto_20160626_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='born_on',
            field=models.DateField(blank=True, null=True, help_text='Data urodzin.'),
        ),
        migrations.AddField(
            model_name='artist',
            name='description_html',
            field=models.TextField(blank=True, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='artist',
            name='description_trevor',
            field=models.TextField(blank=True, null=True, help_text='Krótki opis podmiotu w stylu encyklopedycznym.'),
        ),
        migrations.AddField(
            model_name='artist',
            name='died_on',
            field=models.DateField(blank=True, null=True, help_text='Data śmierci.'),
        ),
        migrations.AddField(
            model_name='artist',
            name='image',
            field=models.ImageField(upload_to='artists', help_text='Ilustracja - zdjęcie artysty.', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='image_source',
            field=models.CharField(help_text='Źródło zdjęcia.', blank=True, null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='artist',
            name='category',
            field=models.IntegerField(choices=[(1, 'Wykonawca własnych tekstów'), (2, 'Kompozytor'), (3, 'Bard zagraniczny'), (4, 'Zespół')], blank=True, null=True, help_text='Kategoria w spisie treści śpiewnika.'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='featured',
            field=models.BooleanField(default=False, help_text='Czy podmiot ma figurować w spisie treści.'),
        ),
    ]
