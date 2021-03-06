from django.contrib import admin

from . import models

admin.site.register(models.MpProfile)

admin.site.register(models.Constituent)

admin.site.register(models.Constituency)

admin.site.register(models.SubAdminPermission)

admin.site.register(models.Region)

admin.site.register(models.Country)
admin.site.register(models.CustomUser)

