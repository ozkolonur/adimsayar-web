from django.contrib import admin
from models import Mailing
from django import forms
from content.models import Content
from mailing.models import *

class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        queryset = Content.objects.filter(page__startswith='mail')
        self.fields['content'] = forms.ModelChoiceField(queryset=queryset, widget=forms.Select)
        obj = kwargs.get("instance", None)
        if not obj is None:
            initial_data = Content.objects.get(page=obj.content)
            self.initial['content'] = initial_data.id

class ElementInline(admin.TabularInline):
    form = MailingForm
    model = Element

class MailingAdmin(admin.ModelAdmin):
    list_display = ('subject','target_date','mail_type','recipient_group')
    inlines = [ElementInline,]


class UserReadMailAdmin(admin.ModelAdmin):
    list_display = ('user','date_time','mailing')
    search_fields = ('user',)


admin.site.register(Mailing, MailingAdmin)
admin.site.register(Element)
admin.site.register(UserReadMail, UserReadMailAdmin)

