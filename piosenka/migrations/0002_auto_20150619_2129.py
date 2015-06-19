# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import piosenka.models


class Migration(migrations.Migration):

    dependencies = [
        ('piosenka', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': ('invite', 'Invite')},
        ),
        migrations.AlterField(
            model_name='invitation',
            name='expires_on',
            field=models.DateTimeField(editable=False, default=piosenka.models._get_default_expires_on),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='invitation_key',
            field=models.CharField(max_length=70, editable=False, default=piosenka.models._get_default_invitation_key),
        ),
    ]
