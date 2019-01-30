# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0006_auto_20160821_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='city',
            field=models.CharField(max_length=200, verbose_name='city'),
        ),
    ]
