# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20150304_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siimciconfig',
            name='poll_repetitions',
            field=models.IntegerField(default=2, verbose_name='poll repetitions', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
