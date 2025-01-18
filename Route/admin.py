from django.contrib import admin
from .models import*

class RouteAdmin(admin.ModelAdmin):
    list_display = ['Route_name','id','Delivery_boy', 'Vehicle_number', 'created_at', 'updated_at', 'created_at','is_deleted']
    
admin.site.register(Route, RouteAdmin)





