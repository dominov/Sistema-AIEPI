# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIIMCIConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(default='SI-IMCI', max_length=255, verbose_name='site name')),
                ('respondents_group', models.ForeignKey(verbose_name='respondents group', to='auth.Group', null=True)),
            ],
            options={
                'verbose_name': 'SI-IMCI Configuration',
                'verbose_name_plural': 'SI-IMCI Configuration',
            },
            bases=(models.Model,),
        ),
    ]
