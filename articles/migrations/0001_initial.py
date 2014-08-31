# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, help_text='Tytuł artykułu, np. \'IX Festiwal Piosenki Poetyckiej im. Jacka Kaczmarskiego "Nadzieja"\'.')),
                ('lead_text_trevor', models.TextField()),
                ('main_text_trevor', models.TextField()),
                ('cover_image', models.ImageField(blank=True, upload_to='article_covers', null=True, help_text='Main illustration for the article.')),
                ('cover_credits_trevor', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True, editable=False)),
                ('date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(default=True, editable=False)),
                ('lead_text_html', models.TextField(editable=False)),
                ('main_text_html', models.TextField(editable=False)),
                ('cover_credits_html', models.TextField(blank=True, null=True, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]
