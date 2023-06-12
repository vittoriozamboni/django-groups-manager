from django.contrib import admin

from groups_manager import models

from mptt.admin import MPTTModelAdmin

admin.site.unregister(models.Group)
admin.site.register(models.Group, MPTTModelAdmin)
