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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text="Tytuł posta, np. 'Nowa wyszukiwarka piosenek.'.", max_length=100)),
                ('post_trevor', models.TextField()),
                ('more_trevor', models.TextField(null=True, blank=True)),
                ('slug', models.SlugField(max_length=100, editable=False, unique=True)),
                ('date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(editable=False, default=True)),
                ('post_html', models.TextField(editable=False, null=True)),
                ('more_html', models.TextField(editable=False, null=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]
