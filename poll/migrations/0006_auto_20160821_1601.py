# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_auto_20160819_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demographics',
            old_name='sector',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='demographics',
            name='education_level',
            field=models.CharField(default=b'1', max_length=1, verbose_name='education level', choices=[(b'3', 'technical'), (b'1', 'Primary'), (b'4', 'Technologist'), (b'2', 'Secondary')]),
        ),
    ]
