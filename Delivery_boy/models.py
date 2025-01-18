from django.db import models

class Delivery_boy(models.Model):
    Code = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Group = models.CharField(max_length=50, blank=True, null=True)
    Home_number = models.CharField(max_length=150, blank=True, null=True)
    Society = models.CharField(max_length=150, blank=True, null=True)
    Area = models.CharField(max_length=150, blank=True, null=True)
    Pincode = models.CharField(max_length=50, blank=True, null=True)
    Moblie1 = models.CharField(max_length=20, blank=True, null=True)
    Moblie2 = models.CharField(max_length=20, blank=True, null=True)
    Email = models.CharField(max_length=50,blank=True, null=True)
    License_number = models.CharField(max_length=50, blank=True, null=True)
    License_lastdate = models.DateField(blank=True, null=True)
    License_type = models.CharField(max_length=50, blank=True, null=True)
    Birth_date = models.CharField(max_length=50, blank=True, null=True)
    Joining_date = models.DateField(blank=True, null=True)
    Current_status = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    Updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.Name
