from django.db import models

# Create your models here.
class Product(models.Model):
    Product_name = models.CharField(max_length=100)
    Hsn_code = models.CharField(max_length=20,null=True, blank=True)
    Product_unit = models.CharField(max_length=20,null=True, blank=True)
    Product_price = models.CharField(max_length=20,null=True, blank=True)
    Previous_stock = models.CharField(max_length=20,null=True, blank=True)
    Minimum_stock = models.CharField(max_length=20,null=True, blank=True)
    Maximum_stock = models.CharField(max_length=20,null=True, blank=True)
    Product_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    Updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
       return self.Product_name   