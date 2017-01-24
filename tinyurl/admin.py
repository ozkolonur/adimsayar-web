from django.contrib import admin

from tinyurl.models import TinyURL

class TinyURLAdmin(admin.ModelAdmin):
    list_display = ('url','hash', 'clicks')


admin.site.register(TinyURL, TinyURLAdmin)

