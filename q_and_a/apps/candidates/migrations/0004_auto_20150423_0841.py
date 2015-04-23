# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0003_candidate_invited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='invited',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
