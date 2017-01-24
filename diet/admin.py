from django.contrib import admin
from diet.models import Diet, DietDefinition, Atom
from django.db import models
from django.forms import forms

class DietInline(admin.TabularInline):  
    model = Atom
    extra = 10

class DietDefinitionAdmin(admin.ModelAdmin):
	formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }
	class Media:
		js = ('/site_media/js/ckeditor/ckeditor.js',)

	inlines = [DietInline]
	list_display = [f.name for f in DietDefinition._meta.fields if f.name!='id']

class AtomAdmin(admin.ModelAdmin):
	list_filter = ['diet__name']
	list_display = [f.name for f in Atom._meta.fields if f.name!='id']

admin.site.register(Diet)
admin.site.register(DietDefinition, DietDefinitionAdmin)
admin.site.register(Atom, AtomAdmin)
