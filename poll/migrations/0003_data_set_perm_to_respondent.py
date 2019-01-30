# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def set_perm(apps, schema_editor):
    Respondent = apps.get_model("poll", "Respondent")
    content_type = ContentType.objects.get_for_model(Respondent)
    is_respondent, created = Permission.objects.get_or_create(content_type=content_type, codename='is_respondent')
    if not is_respondent:
        return
    for respondent in Respondent.objects.all():
        respondent.user.user_permissions.add(is_respondent.id)
        respondent.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('poll', '0002_auto_20160813_1701'),
    ]

    operations = [
        migrations.RunPython(set_perm),
    ]
