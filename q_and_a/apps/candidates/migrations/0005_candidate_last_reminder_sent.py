# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0004_auto_20150423_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='last_reminder_sent',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
