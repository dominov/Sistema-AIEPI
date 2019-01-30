# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_siimciconfig_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siimciconfig',
            name='logo',
            field=models.ImageField(help_text='if this field is fill will replace the site name', upload_to=b'', null=True, verbose_name='logo', blank=True),
        ),
    ]
