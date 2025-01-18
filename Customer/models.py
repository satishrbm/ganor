from django.db import models
from Product.models import Product
from Route.models import Route
from datetime import date, timedelta
# Create your models here.

class Landmark(models.Model):
    landmark = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.landmark}"


class Customers(models.Model):
    DELIVERY_FREQUENCY_CHOICES = [
        ('1', 'Daily'),
        ('2', 'Every Other Day'),
        ('3', 'Weekly'),
    ]

    Order_number = models.IntegerField()
    Sequence = models.IntegerField(null=True, blank=True)
    Stand = models.BooleanField(default=False,null=True, blank=True)
    Customer_name = models.CharField(max_length=100,null=True, blank=True)
    Nick_name = models.CharField(max_length=200,null=True, blank=True)
    C_name = models.CharField(max_length=100,null=True, blank=True)
    N_name = models.CharField(max_length=100, null=True, blank=True)
    work = models.CharField(max_length=200,null=True, blank=True)
    House_number = models.CharField(max_length=200, null=True, blank=True)
    Society = models.CharField(max_length=200, null=True, blank=True)
    Area = models.CharField(max_length=200, null=True, blank=True)
    Pincode = models.CharField(max_length=10, null=True, blank=True)
    Landmark = models.ForeignKey(Landmark,on_delete=models.DO_NOTHING,null=True, blank=True)
    Mobile_number1 = models.CharField(max_length=20,null=True, blank=True)
    Mobile_number2 = models.CharField(max_length=20, null=True, blank=True)
    Email = models.EmailField(null=True, blank=True)
    Reference = models.CharField(max_length=100,null=True, blank=True)
    Started_at = models.DateField(null=True, blank=True)
    End_date = models.DateField(null=True, blank=True)
    Current_status = models.CharField( default='1',max_length=20,null=True, blank=True)
    Restarted_date = models.DateField(null=True, blank=True)
    Morning_bottle = models.FloatField(null=True, blank=True)
    Milk_delivery_frequency = models.CharField(
        max_length=20,
        choices=DELIVERY_FREQUENCY_CHOICES,
        default='1', null=True, blank=True)
    Frequency1 = models.FloatField(blank=True,null=True)
    Frequency2 = models.FloatField(blank=True,null=True)
    Saturday = models.BooleanField(blank=True,null=True,default=False)
    Sunday = models.BooleanField(blank=True,null=True,default=False)
    Further_account = models.FloatField(blank=True,null=True)
    Credit_debit = models.CharField(max_length=20,blank=True,null=True)
    Product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True, blank=True)
    Customer_rate = models.FloatField(null=True, blank=True)
    Cutomer_route = models.ForeignKey(Route,on_delete=models.DO_NOTHING,null=True, blank=True)
    Created_at = models.DateField(auto_now=True,null=True, blank=True)
    Updated_at = models.DateField(null=True, blank=True)
    Total_bottle = models.IntegerField(blank=True,null=True)
    Return_bottle = models.IntegerField(blank=True,null=True)
    is_deleted = models.BooleanField(default=0)

    def __str__(self):
       return self.Customer_name   
    

    def get_latest_sequence_number(self):
        try:
            sequence = Sequence.objects.get(Customer=self)
            return sequence.Sequence_number
        except Sequence.DoesNotExist:
            return None

    def __str__(self):
        return self.Customer_name

    
class Supply(models.Model):
    Customer = models.ForeignKey(Customers,on_delete=models.CASCADE,related_name='supplies')
    Supply_date = models.DateField()
    Today_cost = models.FloatField()
    Today_bottle = models.FloatField()
    Today_return_bottle = models.IntegerField(blank=True)
    Total_cost = models.FloatField()
    Total_bottle = models.IntegerField(blank=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.Customer.Customer_name} {self.Supply_date}"


class Sequence(models.Model):
    Customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
    Route = models.ForeignKey(Route,on_delete=models.CASCADE,blank=True, null= True)
    Sequence_number = models.IntegerField(null=True)
    updated_at = models.DateField(null=True)

    def __str__(self) -> str:
        return f"{self.Sequence_number}"
    

class Customer_products(models.Model):
    Customers = models.ForeignKey(Customers,on_delete=models.CASCADE)
    Customers_product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.Customers}"


class Close_customer(models.Model):
    Customers = models.ForeignKey(Customers,on_delete=models.CASCADE)
    Date = models.DateField(blank=True, null=True)
    Reason = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.Customers}"


class User_delevery(models.Model):
    Customers = models.ForeignKey(Customers,on_delete=models.CASCADE)
    Date = models.DateField(blank=True, null=True)
    milk_need = models.IntegerField(blank=True,null=True)
    created_at = models.DateField(auto_now=True,blank=True,null=True)


    def __str__(self):
        return f"{self.Customers}"
    

