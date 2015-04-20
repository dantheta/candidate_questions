# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_candidate_participating'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='invited',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
