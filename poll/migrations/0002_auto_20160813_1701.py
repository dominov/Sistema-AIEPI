# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='respondent',
            options={'verbose_name': 'respondent', 'verbose_name_plural': 'respondents', 'permissions': (('is_respondent', 'Is respondent'),)},
        ),
    ]
