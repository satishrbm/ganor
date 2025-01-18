from .models import*
from rest_framework import serializers
from Customer.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('id', 'Order_number', 'Customer_name', 'Nick_name', 'C_name', 'N_name')


class BillsSerializer(serializers.ModelSerializer):
    Customer = CustomerSerializer()
    class Meta:
        model = Bills
        fields = '__all__'