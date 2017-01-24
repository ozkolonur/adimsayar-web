# -*- coding: utf-8 -*-
from content.models import *
from django.contrib import admin
from django.db import models
from django import forms

class ContentAdmin(admin.ModelAdmin):
		formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor','style':'width:400px;'})}, }
		list_display = ('title','page')
		class Media:
			js = ('/site_media/js/ckeditor/ckeditor.js',)


class NewsAdmin(admin.ModelAdmin):
		formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor','style':'width:300px;'})}, }
		list_display = ('name','text','date_time',)
		class Media:
			js = ('/site_media/js/ckeditor/ckeditor.js',)


admin.site.register(Content,ContentAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Tweet)
admin.site.register(ActionMsg)
