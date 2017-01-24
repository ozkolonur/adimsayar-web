from models import Device2, Product, Model, Manufacturer
from django.contrib import admin

class Device2Admin(admin.ModelAdmin):
    list_display = ('device_id','appversion','swversion','manufacturer','model','product','user_email', 'date_registered')
    search_fields = ['user','model','product','manufacturer']
    list_filter = ['appversion', 'manufacturer', 'model']

class Model2Admin(admin.ModelAdmin):
    list_display = ('name','manufacturer', 'cnt')
    list_filter = ['manufacturer']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','cnt')

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name','cnt')

admin.site.register(Device2, Device2Admin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Model, Model2Admin)
admin.site.register(Manufacturer, ManufacturerAdmin)





