# -*- coding: utf-8 -*-
from ad.models import *
from django.contrib import admin
from django.db import models
from django import forms

class AdAdmin(admin.ModelAdmin):
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor','style':'width:30px;'})}, }
    list_display = ('name','impression', 'click', 'ctr')
    class Media:
        js = ('/site_media/js/ckeditor/ckeditor.js',)


admin.site.register(Ad, AdAdmin)
admin.site.register(Tag)
