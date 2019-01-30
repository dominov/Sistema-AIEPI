# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0006_remove_siimciconfig_respondents_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='siimciconfig',
            name='copyright',
            field=models.CharField(default=b'SI-IMCI', max_length=255, verbose_name='copyright'),
        ),
    ]
