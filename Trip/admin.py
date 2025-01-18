from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Trip)


class TripAdmin(admin.ModelAdmin):
    list_display = ['Trip_number','id','Trip_date', 'Route_name', 'Vehicle_number', 'Delivery_boy', 'created_at','is_deleted']
    # list_filter = ['Customer', 'Supply_date']
    # search_fields = ['Customer__Customer_name__icontains', 'Supply_date']  # Use Customer__Customer_name__icontains

admin.site.register(Trip, TripAdmin)