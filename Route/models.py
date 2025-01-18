from django.db import models
from Delivery_boy.models import Delivery_boy
from Vehicles.models import Vehicle

# Create your models here.
class Route(models.Model):
    Route_name = models.CharField(max_length=150)
    Delivery_boy = models.ForeignKey(Delivery_boy,on_delete=models.CASCADE)
    Vehicle_number = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.Route_name