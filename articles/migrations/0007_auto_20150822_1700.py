# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_remove_article_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'default_permissions': ['contribute'], 'ordering': ['-pub_date']},
        ),
    ]
