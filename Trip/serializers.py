from rest_framework import serializers
from .models import Trip
from Route.models import Route
from Delivery_boy.models import *
from Vehicles.models import *
from Customer.models import *

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['Trip_number','Trip_date','Route_name','Vehicle_number','Delivery_boy']


class DeliveryBoySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_boy
        fields = ['id', 'Name']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'Vehicle_number']

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'Route_name']


class TripListSerializer(serializers.ModelSerializer):
    Delivery_boy = DeliveryBoySerializer() 
    Vehicle_number = VehicleSerializer() 
    Route_name = RouteSerializer()
    class Meta:
        model = Trip
        fields = ['id','Trip_number','Trip_date','Route_name','Vehicle_number','Delivery_boy']


class OrderNumberSerializer(serializers.Serializer):
    order_number = serializers.CharField()


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'Route_name']


class TripSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['is_deleted']


class CustomerlistSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    class Meta:
        model = Customers
        fields =["id","Customer_name","Nick_name","C_name",'address','N_name','Order_number']

    def get_address(self, obj):
        address_parts = [obj.House_number, obj.Society, obj.Area]
        address_parts = [part for part in address_parts if part]  # Remove empty parts
        return ', '.join(address_parts)

class BulkUpdateCustomerRouteSerializer(serializers.Serializer):
    customer_ids = serializers.ListField(child=serializers.IntegerField())
    new_route_id = serializers.IntegerField()


class ListCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customers
        fields = [
            'id','Cutomer_route','Order_number', 'C_name',
            'Customer_name','N_name'
        ]


#=================================================================================

class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ['Customer', 'Supply_date', 'Today_bottle']