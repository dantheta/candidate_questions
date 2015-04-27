# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_candidate_last_reminder_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'NEW'), (1, b'INVITED'), (2, b'PARTICIPATING'), (3, b'DECLINED')]),
            preserve_default=True,
        ),
    ]
