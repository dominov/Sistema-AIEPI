# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20160816_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demographics',
            name='education_level',
            field=models.CharField(default=b'1', max_length=1, verbose_name='education level', choices=[(b'1', 'Primary'), (b'2', 'Secondary'), (b'3', 'technical'), (b'4', 'Technologist')]),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='gender',
            field=models.CharField(default=b'F', max_length=1, verbose_name='gender', choices=[(b'F', 'Female'), (b'M', 'Male')]),
        ),
    ]
