from django.contrib import admin

from badges.models import Badge,BadgeToUser

class BadgeAdmin(admin.ModelAdmin):
    fields = ('icon',)
    list_display = ('id','level')

class BadgeToUserAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('badge','user', 'created')


admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeToUser, BadgeToUserAdmin)
