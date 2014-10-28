from django.contrib import admin

import models


admin.site.register(models.Member)
admin.site.register(models.Group)
admin.site.register(models.GroupType)
admin.site.register(models.GroupEntity)
admin.site.register(models.GroupMember)
admin.site.register(models.GroupMemberRole)
