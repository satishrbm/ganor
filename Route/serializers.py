from rest_framework import serializers
from .models import*


class DeliveryBoySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_boy
        fields = ['id', 'Name']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'Vehicle_number']


class RouteListSerializer(serializers.ModelSerializer):
    Delivery_boy = DeliveryBoySerializer()  # SerializerMethodField for Delivery_boy
    Vehicle_number = VehicleSerializer()  # SerializerMethodField for Vehicle_number

    class Meta:
        model = Route
        fields = ['id','Route_name', 'Delivery_boy', 'Vehicle_number']



class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['Route_name', 'Delivery_boy', 'Vehicle_number']

class RouteEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id','Route_name', 'Delivery_boy', 'Vehicle_number','updated_at']

class RouteDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['is_deleted']
