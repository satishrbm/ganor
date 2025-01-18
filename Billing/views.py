from django.shortcuts import render
from Customer.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
from django.db.models import Sum
from .serializers import BillsSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Max
from rest_framework import generics


def route_customer(request, route_id, from_date=None, to_date=None):
    from_date = datetime.strptime(from_date, '%Y-%m-%d') if from_date else None
    to_date = datetime.strptime(to_date, '%Y-%m-%d') if to_date else None
    supplies = Supply.objects.filter(Customer__Cutomer_route__id=route_id, Supply_date__range=(from_date, to_date)).values('Customer_id').annotate(total_bottles=Sum('Today_bottle'))

    response_data = []
    for supply in supplies:
        customer = Customers.objects.get(pk=supply['Customer_id'])
        total_bottles = supply['total_bottles'] or 0  
        milk_price = customer.Customer_rate
        total_cost = milk_price * total_bottles
        
        response_data.append({
            'customer_id': customer.id,
            'customer_number': customer.Order_number,
            'milk_price': milk_price,
            'name': customer.C_name,
            'total_bottles': total_bottles,
            'total_cost': total_cost
        })
    return JsonResponse(response_data, safe=False)




def generate_bill_api(request, route_id, from_date=None, to_date=None):
    data = generate_bill(request, route_id, from_date, to_date)
    return JsonResponse(data)



def generate_bill_number():
    last_bill = Bills.objects.aggregate(Max('Bill_number'))['Bill_number__max']
    if last_bill:
        new_bill_number = int(last_bill) + 1
    else:
        new_bill_number = 1111111111
    return str(new_bill_number).zfill(10)

@api_view(['POST'])
def generate_bill(request):
    if request.method == 'POST':
        customer_ids = request.data.get('customer_ids', [])
        from_date_str = request.data.get('from_date')
        to_date_str = request.data.get('to_date')

        if not customer_ids:
            return Response({'error': 'No customer IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else None
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else None

        response_data = []

        for customer_id in customer_ids:
            supplies = Supply.objects.filter(Customer__id=customer_id, Supply_date__range=(from_date, to_date)).values('Customer_id').annotate(total_bottles=Sum('Today_bottle'))
            print(supplies)
            for supply in supplies:
                customer = Customers.objects.get(pk=supply['Customer_id'])
                total_bottles = supply['total_bottles'] or 0  
                milk_price = customer.Customer_rate
                total_cost = milk_price * total_bottles
                
                bill_number = generate_bill_number()

                bill = Bills.objects.create(
                    Customer=customer,
                    Bill_number=bill_number,
                    bill_date=datetime.now(),
                    from_date=from_date,
                    to_date=to_date,
                    bottle_couont=total_bottles,
                    rate=milk_price,
                    count_total=total_cost,
                    baaki_jamaa=0, 
                    final_price=total_cost
                )
                response_data.append(BillsSerializer(bill).data)

        return Response(response_data, status=status.HTTP_200_OK)  # Return Response object
    else:
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get bills 


class BillsListView(generics.ListAPIView):
    serializer_class = BillsSerializer

    def get_queryset(self):
        queryset = Bills.objects.all()
        
        # Get query parameters
        route_id = self.request.query_params.get('route', None)
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        
        # Filter queryset based on parameters
        if route_id:
            queryset = queryset.filter(Customer__Cutomer_route_id=route_id)
        if from_date:
            queryset = queryset.filter(bill_date__gte=from_date)
        if to_date:
            queryset = queryset.filter(bill_date__lte=to_date)
        
        return queryset

#===================================================================================

@api_view(['GET'])
def customer_bill_list(request, customer_id):
    """
    List all bills for a particular customer.
    """
    bills = Bills.objects.filter(Customer_id=customer_id).order_by('-bill_date')
    serializer = BillsSerializer(bills, many=True)
    return Response(serializer.data)