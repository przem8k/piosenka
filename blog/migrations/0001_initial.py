# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import content.slug


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('slug', models.SlugField(max_length=100, unique=True, editable=False)),
                ('title', models.CharField(max_length=100, help_text="Tytuł posta, np. 'Nowa wyszukiwarka piosenek.'.")),
                ('post_trevor', models.TextField()),
                ('more_trevor', models.TextField(null=True, blank=True)),
                ('post_html', models.TextField(null=True, editable=False)),
                ('more_html', models.TextField(null=True, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['-pub_date'],
                'default_permissions': ['contribute'],
                'abstract': False,
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
    ]
