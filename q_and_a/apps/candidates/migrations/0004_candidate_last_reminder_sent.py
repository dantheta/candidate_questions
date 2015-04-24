# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0003_candidate_invited'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='last_reminder_sent',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
