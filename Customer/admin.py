from django.contrib import admin
from .models import *
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','Customer_name','Order_number']

admin.site.register(Customers, CustomerAdmin)



class SequenceAdmin(admin.ModelAdmin):
    list_display = ['id','Customer', 'Route', 'Sequence_number', 'updated_at']
    
admin.site.register(Sequence,SequenceAdmin)



class SupplyAdmin(admin.ModelAdmin):
    list_display = ['id','Customer', 'Supply_date', 'Today_cost', 'Today_bottle', 'Total_cost', 'updated_at']
    list_filter = ['Customer', 'Supply_date']
    search_fields = ['Customer__Customer_name__icontains', 'Supply_date']  # Use Customer__Customer_name__icontains

admin.site.register(Supply, SupplyAdmin)



class LandmarkAdmin(admin.ModelAdmin):
    list_display = ['landmark','id']
    
admin.site.register(Landmark,LandmarkAdmin)




class Close_customerAdmin(admin.ModelAdmin):
    list_display = ['Customers','Date','Reason']
    
admin.site.register(Close_customer,Close_customerAdmin)

class User_deleveryAdmin(admin.ModelAdmin):
    list_display = ['Customers','Date','milk_need','created_at']
    
admin.site.register(User_delevery,User_deleveryAdmin)