# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('articles', '0001_initial'), ('articles', '0002_auto_20141205_2356'), ('articles', '0003_auto_20141213_1704'), ('articles', '0004_auto_20141221_2053'), ('articles', '0005_auto_20141221_2255'), ('articles', '0006_remove_article_published'), ('articles', '0007_auto_20150822_1700')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100, help_text='Tytuł artykułu, np. \'IX Festiwal Piosenki Poetyckiej im. Jacka Kaczmarskiego "Nadzieja"\'.')),
                ('lead_text_trevor', models.TextField()),
                ('main_text_trevor', models.TextField()),
                ('cover_image', models.ImageField(upload_to='article_covers', blank=True, help_text='Main illustration for the article.', null=True)),
                ('cover_credits_trevor', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=100, editable=False, unique=True)),
                ('date', models.DateTimeField(editable=False)),
                ('published', models.BooleanField(editable=False, default=True)),
                ('lead_text_html', models.TextField(editable=False)),
                ('main_text_html', models.TextField(editable=False)),
                ('cover_credits_html', models.TextField(editable=False, blank=True, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date']},
        ),
        migrations.RenameField(
            model_name='article',
            old_name='date',
            new_name='pub_date',
        ),
        migrations.AddField(
            model_name='article',
            name='reviewed',
            field=models.BooleanField(editable=False, default=False),
        ),
        migrations.RemoveField(
            model_name='article',
            name='published',
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date'], 'default_permissions': ['contribute']},
        ),
    ]
