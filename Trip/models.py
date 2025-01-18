from django.db import models
from Route.models import Route
from Vehicles.models import Vehicle
from Delivery_boy.models import Delivery_boy
from Customer.models import Customers
# Create your models here.
class Trip(models.Model):
    Trip_number = models.CharField(max_length=100)
    Trip_date = models.DateField()
    Route_name = models.ForeignKey(Route,on_delete=models.DO_NOTHING)
    Vehicle_number = models.ForeignKey(Vehicle,on_delete=models.DO_NOTHING)
    Delivery_boy = models.ForeignKey(Delivery_boy,on_delete=models.DO_NOTHING)
    Customer_list = models.ManyToManyField(Customers,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
       return str(self.Trip_number)