# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_auto_20150628_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siimciconfig',
            name='respondents_group',
        ),
    ]
