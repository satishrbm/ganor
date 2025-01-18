from rest_framework import serializers
from .models import *

class Delivery_boySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_boy
        fields = ["Code", "Name", "Group", "Home_number", "Society", "Area", "Pincode", "Moblie1",
                   "Moblie2", "Email", "License_number", "License_lastdate", "License_type",
                   "Birth_date", "Joining_date", "Current_status", "is_active"]


class EditDelivery_boySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_boy
        fields = ["Code", "Name", "Group", "Home_number", "Society", "Area", "Pincode", "Moblie1",
                   "Moblie2", "Email", "License_number", "License_lastdate", "License_type",
                   "Birth_date", "Joining_date", "Current_status", "is_active","Updated_at"]

class Delivery_boyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_boy
        fields = ["id","Code", "Name", "Group", "Home_number", "Society", "Area", "Pincode", "Moblie1",
                   "Moblie2", "Email", "License_number", "License_lastdate", "License_type",
                   "Birth_date", "Joining_date", "Current_status", "is_active"]

class OrderNumberSerializer(serializers.Serializer):
    order_number = serializers.CharField()

