# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(help_text='Description, written in Markdown.')),
                ('description_html', models.TextField(editable=False, null=True, blank=True)),
                ('position', models.IntegerField()),
                ('image', models.ImageField(upload_to='carousel_items', help_text='Picture to display in carousel.')),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
    ]
