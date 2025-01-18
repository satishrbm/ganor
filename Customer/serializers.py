from rest_framework import serializers
from .models import *
from Route.models import Route



class CustomerRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['Route_name', 'id']

class OrderNumberSerializer(serializers.Serializer):
    order_number = serializers.CharField()

class ReStartCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields=['Current_status','Restarted_date']


class AddCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields=['Order_number','Stand','Customer_name','Nick_name','C_name','N_name','work',
        'House_number','Society','Area','Pincode','Mobile_number1','Mobile_number2',
        'Email','Started_at','Current_status','Morning_bottle','Frequency1','Frequency2',
        'Sunday','Saturday','Landmark','Product','Customer_rate','Cutomer_route','Reference'
        ]



class ListCustomerSerializer(serializers.ModelSerializer):
    Sequence_Number = serializers.SerializerMethodField()
    Cutomer_route = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = [
            'id', 'Sequence_Number', 'Cutomer_route','Order_number', 'C_name',
            'N_name','Mobile_number1'
        ]

    def get_Sequence_Number(self, obj):
        return obj.get_latest_sequence_number()

    def get_Cutomer_route(self, obj):
        if obj.Cutomer_route:
            return obj.Cutomer_route.Route_name
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        for key, value in data.items():
            if value is None:
                data[key] = ''  # Set the value to an empty string for fields with null values

        return data


class DeleteCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields=['id','is_deleted']


class EditCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields=['id','Order_number','Stand','Customer_name','Nick_name','C_name','N_name','work',
        'House_number','Society','Area','Started_at','Pincode','Mobile_number1','Mobile_number2',
        'Email','Started_at','Current_status','Morning_bottle','Frequency1','Frequency2',
        'Sunday','Saturday','Landmark','Product','Customer_rate','Cutomer_route','Reference'
        ]

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = ['Customer', 'Sequence_number','updated_at']


class BottleCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['id','Total_bottle']


class CustomerUpdateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    Total_bottle = serializers.IntegerField()


class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = ['id','landmark']


class CloseCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Close_customer
        fields = ['Customers','Date','Reason']


# class CloseCustomerkListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Close_customer
#         fields = ['Customers','Date','Reason']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers  # Assuming that's the name of your Customer model
        fields = ['id','Order_number', 'C_name']

class CloseCustomerkListSerializer(serializers.ModelSerializer):
    Customers = CustomerSerializer(read_only=True)

    class Meta:
        model = Close_customer
        fields = ['Customers', 'Date', 'Reason']



class UserDeleverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User_delevery
        fields = ['Customers', 'Date', 'milk_need']