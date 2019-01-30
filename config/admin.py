from django.contrib import admin

from solo.admin import SingletonModelAdmin

from config.models import SIIMCIConfig

admin.site.register(SIIMCIConfig, SingletonModelAdmin)
