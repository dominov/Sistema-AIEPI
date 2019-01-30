# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_data_set_perm_to_respondent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='polldate',
            options={'ordering': ['order'], 'verbose_name': 'poll date', 'verbose_name_plural': 'poll dates'},
        ),
    ]
