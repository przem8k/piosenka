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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Tytuł artykułu, np. \'IX Festiwal Piosenki Poetyckiej im. Jacka Kaczmarskiego "Nadzieja"\'.', max_length=100)),
                ('lead_text_trevor', models.TextField()),
                ('main_text_trevor', models.TextField()),
                ('cover_image', models.ImageField(upload_to='article_covers', help_text='Main illustration for the article.', null=True, blank=True)),
                ('cover_credits_trevor', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(max_length=100, editable=False, unique=True)),
                ('date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(editable=False, default=True)),
                ('lead_text_html', models.TextField(editable=False)),
                ('main_text_html', models.TextField(editable=False)),
                ('cover_credits_html', models.TextField(editable=False, null=True, blank=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]
