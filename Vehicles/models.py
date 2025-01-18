from django.db import models

class Vehicle(models.Model):
   
    Vehicle_type = models.CharField(max_length=128)
    Vehicle_number = models.CharField(max_length=128)
    Vehicle_owner = models.CharField(max_length=128)
    Vehicle_owner_type = models.CharField(max_length=128)
    Vehicle_price = models.FloatField(max_length=128)
    Vehicle_purchase_date = models.CharField(max_length=128)
    Vehicle_average = models.CharField(max_length=128)
    Vehicle_puc = models.CharField(max_length=128)
    Vehicle_puc_date = models.CharField(max_length=128)
    Vehicle_insurance = models.CharField(max_length=128)
    Vehicle_insurance_date = models.CharField(max_length=128)
    Vehicle_status = models.BooleanField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.Vehicle_type
