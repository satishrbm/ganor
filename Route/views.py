from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from .serializers import RouteSerializer
from .models import Route
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from Customer.models import Customers,Supply
from datetime import datetime
#==========================================================================================

class RouteListView(generics.ListAPIView):
    serializer_class = RouteListSerializer

    def get_queryset(self):
        return Route.objects.filter(is_deleted=False)


#==========================================================================================

class RouteCreateView(generics.CreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    'success': True,
                    'message': 'Route created successfully.',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {
                    'success': True,
                    'message': 'Validation error.',
                    'errors': e.detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )



#==========================================================================================

class RouteDeleteView(generics.DestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteDeleteSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"message": "Route deleted successfully."})

#==========================================================================================

class RouteUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteEditSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Route updated successfully',
        }, status=status.HTTP_200_OK)


#==========================================================================================


class DeliveryBoyListView(generics.ListAPIView):
    serializer_class = DeliveryBoySerializer

    def get_queryset(self):
        return Delivery_boy.objects.filter(is_deleted=False)

class VehicleListView(generics.ListAPIView):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return Vehicle.objects.filter(is_deleted=False)


#==========================================================================================


class getdata(APIView):
    def get(self, request, route_id):
        customers = Customers.objects.filter(Cutomer_route__id=route_id,is_deleted=False)
        customer_data = [
            {
                'id': customer.id,
                'name': customer.Customer_name,
                'Total_bottle':customer.Total_bottle,

            }
            for customer in customers
        ]

        return Response({
            'customer_data': customer_data

        })


#=============================================================================================



class getCustomerdata(APIView):
    def get(self, request, customer_id):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        customers = Customers.objects.filter(id=customer_id, is_deleted=False)

        supplies_data_list = []
        for customer in customers:
            supplies = Supply.objects.filter(Customer_id=customer.id, Supply_date__range=(start_date, end_date))
            supplies_data = [
                {
                    'supply_id': supply.id,
                    'customer_id': supply.Customer.id,
                    'Supply_date': supply.Supply_date,
                    'Today_bottle': supply.Today_bottle
                }
                for supply in supplies
            ]
            supplies_data_list.extend(supplies_data)
        customer_data = [
            {
                'id': customer.id,
                'name': customer.Customer_name,
                'Total_bottle': customer.Total_bottle,
            }
            for customer in customers
        ]

        return Response({
            'customer_data': customer_data,
            'supplies_data_list': supplies_data_list
        })
