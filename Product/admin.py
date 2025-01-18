from django.contrib import admin
from Product.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','Product_name']
    
admin.site.register(Product,ProductAdmin)