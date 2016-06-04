# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FbEvent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('fb_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField()),
                ('town', models.CharField(max_length=100)),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='performer',
            name='fb_page_id',
            field=models.CharField(blank=True, null=True, max_length=100, unique=True),
        ),
    ]
