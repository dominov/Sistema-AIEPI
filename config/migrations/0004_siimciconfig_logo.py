# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_auto_20150308_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='siimciconfig',
            name='logo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='logo', blank=True),
            preserve_default=True,
        ),
    ]
