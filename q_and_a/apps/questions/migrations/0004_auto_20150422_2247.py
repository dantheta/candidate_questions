# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20150416_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='completed_timestamp',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
