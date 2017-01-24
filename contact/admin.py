from django.contrib import admin
from contact.models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','subject','from_email','auto_replied','answered')
    list_editable = ('answered',)

admin.site.register(Contact,ContactAdmin)