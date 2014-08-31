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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, help_text="Tytuł posta, np. 'Nowa wyszukiwarka piosenek.'.")),
                ('post_trevor', models.TextField()),
                ('more_trevor', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=100, unique=True, editable=False)),
                ('date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(default=True, editable=False)),
                ('post_html', models.TextField(null=True, editable=False)),
                ('more_html', models.TextField(null=True, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]
