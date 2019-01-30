# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siimciconfig',
            name='create_date',
            field=models.DateField(auto_now_add=True, verbose_name='create date', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='siimciconfig',
            name='last_modified',
            field=models.DateField(auto_now=True, verbose_name='last-modified', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='siimciconfig',
            name='poll_repetitions',
            field=models.IntegerField(default=2, verbose_name='poll repetitions'),
            preserve_default=True,
        ),
    ]
