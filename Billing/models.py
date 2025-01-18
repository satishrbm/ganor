from django.db import models
from Customer.models import *

# Create your models here.
class Bills(models.Model):
    Customer = models.ForeignKey(Customers,on_delete=models.DO_NOTHING)
    Bill_number = models.CharField(max_length = 200, blank=True)
    bill_date = models.DateField(auto_now=True)
    from_date = models.DateField()
    to_date = models.DateField()
    details = models.CharField(max_length = 200, blank=True)
    bottle_couont = models.IntegerField(blank=True)
    rate = models.FloatField()
    count_total = models.FloatField()
    baaki_jamaa = models.FloatField()
    final_price = models.FloatField()
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(null=True, blank = True)

    def __str__(self):
        return str(self.Bill_number)