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
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('reviewed', models.BooleanField(editable=False, default=False)),
                ('pub_date', models.DateTimeField(editable=False)),
                ('slug', models.SlugField(editable=False, unique=True, max_length=100)),
                ('title', models.CharField(help_text='Tytuł artykułu, np. \'IX Festiwal Piosenki Poetyckiej im. Jacka Kaczmarskiego "Nadzieja"\'.', max_length=100)),
                ('lead_text_trevor', models.TextField()),
                ('main_text_trevor', models.TextField()),
                ('cover_image', models.ImageField(upload_to='article_covers', help_text='Main illustration for the article.', blank=True, null=True)),
                ('cover_credits_trevor', models.TextField(null=True, blank=True)),
                ('lead_text_html', models.TextField(editable=False)),
                ('main_text_html', models.TextField(editable=False)),
                ('cover_credits_html', models.TextField(editable=False, null=True, blank=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pub_date'],
                'abstract': False,
                'default_permissions': ['contribute'],
            },
            bases=(content.slug.SlugLogicMixin, models.Model),
        ),
    ]
