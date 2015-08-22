# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_post_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'default_permissions': ['contribute'], 'ordering': ['-pub_date']},
        ),
    ]
