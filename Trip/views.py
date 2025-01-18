from rest_framework import generics, status
from .models import Trip
from .serializers import * 
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Delivery_boy, Vehicle
from django.db.models import Max
from rest_framework.decorators import api_view
from Customer.models import *
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from datetime import datetime
from datetime import date
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_order_number(request):
    last_order_number = Trip.objects.aggregate(Max('Trip_number'))['Trip_number__max']

    if last_order_number:
        last_number = int(last_order_number[1:])  # Remove the prefix and convert to integer
        new_number = last_number + 1
        order_number = '0{:04d}'.format(new_number)  # Format the new number with leading zeros and prefix
    else:
        order_number = '00001'  # First order number

    serializer = OrderNumberSerializer({'order_number': order_number})
    return Response(serializer.data)

#====================================================================================


class Customer:
    def __init__(self, started_at, frequency1, frequency2):
        self.Started_at = started_at
        self.Frequency1 = frequency1
        self.Frequency2 = frequency2

def generate_schedule(customer):
    schedule = {}
    current_bottle_count = customer.Frequency1
    for day in range(1, 32):  
        schedule[day] = current_bottle_count
        current_bottle_count = customer.Frequency2 if current_bottle_count == customer.Frequency1 else customer.Frequency1
    return schedule

def calculate_today_bottle(customer, trip_date):
    day_of_week = trip_date.weekday() 
    day_of_month = trip_date.day    
    if (day_of_week == 5 and customer.Saturday) or (day_of_week == 6 and customer.Sunday):
        return 0    
    schedule = generate_schedule(customer)
    return schedule.get(day_of_month, 0)

started_at = date(2023, 8, 18)
frequency1 = 5
frequency2 = 0
customer = Customer(started_at, frequency1, frequency2)
trip_date = date(2023, 8, 18)  # Example date
today_bottle = calculate_today_bottle(customer, trip_date)

#====================================================================================



class TripCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if a trip already exists for the given date and route
        trip_date = serializer.validated_data['Trip_date']
        route_name = serializer.validated_data['Route_name']
        existing_trip = Trip.objects.filter(Trip_date=trip_date, Route_name=route_name).first()

        if existing_trip:
            return Response(
                {'status': 'error', 'message': 'Trip already exists for this date and route.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        customers = Customers.objects.filter(Cutomer_route__Route_name=route_name)
        response_data = []
        for customer in customers:
            supply = Supply()
            supply.Customer = customer
            supply.Supply_date = trip_date
            supply.Today_bottle = calculatetodaybottle(customer, trip_date)
            supply.Today_cost = customer.Customer_rate * supply.Today_bottle
            supply.Today_return_bottle = 0

            last_supply = Supply.objects.filter(Customer=customer).order_by('-Supply_date').first()
            last_total_bottle = last_supply.Total_bottle if last_supply else 0            
            supply.Total_bottle = supply.Today_bottle + last_total_bottle             
            supply.Total_cost = supply.Today_cost
            supply.updated_at = timezone.now()
            supply.save()

            # Check if there is a 'User_delevery' record for the customer on the 'trip_date'
            try:
                user_delivery = User_delevery.objects.get(Customers=customer, Date=trip_date)
                flag = 1  # User_delevery record found
            except User_delevery.DoesNotExist:
                flag = 0  # No User_delevery record found

            response_data.append({
                'customer_id': customer.id,
                'flag': flag,
                # Add other fields as needed
            })

        return Response(
            {
                'status': 'success',
                'message': 'Trip created successfully.',
                'data': serializer.data,
                'customer_data': response_data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
#====================================================================================

class getdata(APIView):
    def get(self, request, route_id):
        current_date = date.today()

        delivery_boys = Delivery_boy.objects.filter(route__id=route_id, is_deleted=False)
        vehicles = Vehicle.objects.filter(route__id=route_id, is_deleted=False)
        customers = Customers.objects.filter(Cutomer_route__id=route_id, is_deleted=False, Current_status=1)
        data_list = []
        total_bottle_all = 0
        tomorrow_bottle_all = 0
        milk_need_today_all = 0

        for customer in customers:
            last_supply = Supply.objects.filter(Customer=customer).order_by('-Supply_date').first()
            total_bottle = 0
            if last_supply:
                total_bottle = last_supply.Total_bottle

            milk_need = calculatetodaybottle(customer, current_date)
            tomorrow_date = current_date + timedelta(days=1)
            tomorrow_bottle = calculatetodaybottle(customer, tomorrow_date)

            try:
                user_delivery = User_delevery.objects.get(Customers=customer, Date=current_date)
                flag_today = 1  # Set flag to 1 if User_delevery record is found
            except User_delevery.DoesNotExist:
                flag_today = 0 

            total_bottle_all += total_bottle
            tomorrow_bottle_all += tomorrow_bottle
            milk_need_today_all += milk_need
            
            data_list.append({
                'customer_id': customer.id,
                'customer_number': customer.Order_number,
                'name': customer.Nick_name,
                'nick_name':customer.N_name,
                'sequence_number': customer.get_latest_sequence_number(),
                'total_bottle': total_bottle,
                'tommorrow_bottle': tomorrow_bottle,
                'milk_need_today': milk_need,
                'flag_today': flag_today,
            })
        delivery_boy_data = [{'id': delivery_boy.id, 'name': delivery_boy.Name} for delivery_boy in delivery_boys]
        vehicle_data = [{'id': vehicle.id, 'name': vehicle.Vehicle_number} for vehicle in vehicles]

        return Response({
            'delivery_boys': delivery_boy_data,
            'vehicles': vehicle_data,
            'customer_data_list': data_list,
            'total_bottle_all': total_bottle_all,
            'tomorrow_bottle_all': tomorrow_bottle_all,
            'milk_need_today_all': milk_need_today_all,
        })
#====================================================================================



class RouteListView(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


#====================================================================================

class TripListView(generics.ListAPIView):
    serializer_class = TripListSerializer

    def get_queryset(self):
        return Trip.objects.filter(is_deleted=False)
    

#====================================================================================



class CusstomerList(generics.ListAPIView):
    serializer_class = CustomerlistSerializer

    def get_queryset(self):
        return Customers.objects.filter(is_deleted=False,Current_status=1)


#====================================================================================
    

class TripDeleteView(generics.DestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializerDelete

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "Trip deleted successfully."},
            status=status.HTTP_200_OK)
    
#====================================================================================

class BulkUpdateCustomersRoute(APIView):
    def put(self, request):
        serializer = BulkUpdateCustomerRouteSerializer(data=request.data)
        if serializer.is_valid():
            customer_ids = serializer.validated_data['customer_ids']
            new_route_id = serializer.validated_data['new_route_id']

            customers = Customers.objects.filter(pk__in=customer_ids)
            if not customers.exists():
                return Response({"message": "Customers not found."}, status=status.HTTP_404_NOT_FOUND)

            customers.update(Cutomer_route=new_route_id)
            return Response({"message": "Customers' routes updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#====================================================================================


#Milk_Applicagtion

#====================================================================================


def generateschedule(customer):
    schedule = {}
    current_bottle_count = customer.Frequency1

    for day in range(1, 32):
        schedule[day] = current_bottle_count

        current_bottle_count = customer.Frequency2 if current_bottle_count == customer.Frequency1 else customer.Frequency1

    return schedule

def get_total_bottle(customer, trip_date):
    try:
        supply = Supply.objects.get(Customer=customer, Supply_date=trip_date)
        return supply.Total_bottle
    except Supply.DoesNotExist:
        return 0  # Return 0 if no supply data available for the customer on the specified date

def calculatetodaybottle(customer, trip_date):
    day_of_week = trip_date.weekday()  # 0 = Monday, 6 = Sunday
    day_of_month = trip_date.day

    # Check if there is a 'User_delevery' record for the customer on the 'trip_date'
    try:
        user_delivery = User_delevery.objects.get(Customers=customer, Date=trip_date)
        return user_delivery.milk_need
    except User_delevery.DoesNotExist:
        pass  # No User_delevery record found, so we continue

    if (day_of_week == 5 and customer.Saturday) or (day_of_week == 6 and customer.Sunday):
        return 0

    schedule = generateschedule(customer)
    return schedule.get(day_of_month, 0)

def generate_two_months_schedule(request, customer_id):
    try:
        customer = Customers.objects.get(id=customer_id)
    except Customers.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

    current_date = date.today()

    first_day_of_current_month = date(current_date.year, current_date.month, 1)
    last_day_of_current_month = date(current_date.year, current_date.month, 1) + timedelta(days=31)

    next_month = current_date.replace(day=1) + timedelta(days=32)
    first_day_of_next_month = date(next_month.year, next_month.month, 1)
    last_day_of_next_month = date(next_month.year, next_month.month, 1) + timedelta(days=31)

    two_months_schedule = {}
    current_date = first_day_of_current_month

    while current_date <= last_day_of_next_month:
        total_bottle = get_total_bottle(customer, current_date)
        two_months_schedule[current_date.strftime('%d-%m-%Y')] = {
            'total_bottle': total_bottle,
            'milk_need': calculatetodaybottle(customer, current_date)
        }
        current_date += timedelta(days=1)

    data = {'two_months_schedule': two_months_schedule}

    return JsonResponse(data)



#==========================================================================

class customersearch(generics.ListAPIView):
    serializer_class = ListCustomerSerializer

    def get_queryset(self):        
        return Customers.objects.filter(is_deleted=False, Current_status=1)
    

#========================================================================

# class UpdateSupplyAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         customer_id = request.data.get('customer_id')
#         supply_date = request.data.get('supply_date')
#         today_bottle = request.data.get('today_bottle')

#         try:
#             supply = Supply.objects.get(Customer__id=customer_id, Supply_date=supply_date)
#             supply.Today_bottle = today_bottle
#             supply.save()

#             serializer = SupplySerializer(supply)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Supply.DoesNotExist:
#             return Response({"error": "Supply record not found."}, status=status.HTTP_404_NOT_FOUND)
    

from django.db.models import F

class UpdateSupplyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')
        supply_date = request.data.get('supply_date')
        today_bottle = float(request.data.get('today_bottle'))

        try:
            supply = Supply.objects.get(Customer__id=customer_id, Supply_date=supply_date)

            # Calculate the difference between the new today_bottle and the existing Today_bottle
            bottle_difference = today_bottle - float(supply.Today_bottle)

            # Update Today_bottle and Total_bottle fields
            supply.Today_bottle = today_bottle
            supply.Total_bottle = F('Total_bottle') + bottle_difference

            # Save the supply object
            supply.save()

            serializer = SupplySerializer(supply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Supply.DoesNotExist:
            return Response({"error": "Supply record not found."}, status=status.HTTP_404_NOT_FOUND)


class get_route_customers_data(APIView):
    def get(self, request, route_id):
        customers = Customers.objects.filter(Cutomer_route__id=route_id, is_deleted=False, Current_status=1)
        data_list = []

        for customer in customers:           
            data_list.append({
                'customer_id': customer.id,
                'customer_number': customer.Order_number,
                'name': customer.Nick_name,
                'nick_name':customer.N_name,
            })

        return Response({
            'customer_data_list': data_list,
        })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def update_today_return_bottle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for entry in data:
                customer_id = entry.get('Customer')
                supply_date = entry.get('Supply_date')
                today_return_bottle = entry.get('Today_return_bottle')

                # Assuming your Supply model has an 'id' field
                supply_instance = Supply.objects.get(Customer__id=customer_id, Supply_date=supply_date)

                # Update the Today_return_bottle field
                supply_instance.Today_return_bottle = today_return_bottle

                # Calculate Today_bottle
                supply_instance.Total_bottle = supply_instance.Total_bottle - today_return_bottle

                supply_instance.save()

            return JsonResponse({'message': 'Success', 'details': 'Data updated successfully.'})
        except ObjectDoesNotExist as e:
            return JsonResponse({'message': 'Failed', 'details': f'Data not found. Error: {str(e)}'})
        except Exception as e:
            return JsonResponse({'message': 'Failed', 'details': f'An error occurred. Error: {str(e)}'})
    else:
        return JsonResponse({'message': 'Failed', 'details': 'Invalid request method. Use POST.'})
    

#====================================================================================
    
def generate_schedule(customer):
    schedule = {}
    current_bottle_count = customer.Frequency1

    for day in range(1, 32):
        schedule[day] = current_bottle_count

        current_bottle_count = customer.Frequency2 if current_bottle_count == customer.Frequency1 else customer.Frequency1

    return schedule


def calculate_bottle(customer, trip_date):
    day_of_week = trip_date.weekday()  # 0 = Monday, 6 = Sunday
    day_of_month = trip_date.day 
    try:
        user_delivery = User_delevery.objects.get(Customers=customer, Date=trip_date)
        return user_delivery.milk_need
    except User_delevery.DoesNotExist:
        pass 

    if (day_of_week == 5 and customer.Saturday) or (day_of_week == 6 and customer.Sunday):
        return 0

    schedule = generate_schedule(customer)
    return schedule.get(day_of_month, 0)


class trip_slip(APIView):
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
       
        customers = Customers.objects.filter(Cutomer_route=trip.Route_name, is_deleted=False, Current_status=1)
        data_list = []    

        for customer in customers:
            # last_supply = Supply.objects.filter(Customer=customer).order_by('-Supply_date').first()
            last_supply = Supply.objects.filter(Customer=customer, Supply_date=trip.Trip_date).first()

            total_given_bottle = 0
            if last_supply:
                total_given_bottle = last_supply.Total_bottle

            milk_need = calculate_bottle(customer, trip.Trip_date)
            tomorrow_date = trip.Trip_date + timedelta(days=1)
            tomorrow_bottle = calculate_bottle(customer, tomorrow_date)

            try:
                user_delivery = User_delevery.objects.get(Customers=customer, Date=trip.Trip_date)
                flag = 1  
            except User_delevery.DoesNotExist:
                flag = 0         

            data_list.append({
                'customer_id': customer.id,
                'customer_number': customer.Order_number,
                'name': customer.Nick_name,
                'nick_name': customer.N_name,
                'sequence_number': customer.get_latest_sequence_number(),
                'total_given_bottle': total_given_bottle,
                'tommorrow_bottle': tomorrow_bottle,
                # 'milk_need_today': milk_need,
                'flag': flag,
            })      

        return Response({
            'trip_data': {
                'trip_number': trip.Trip_number,
                'trip_date': trip.Trip_date,
                'route_name': trip.Route_name.Route_name,  
                'vehicle_number': trip.Vehicle_number.Vehicle_number, 
                'delivery_boy': trip.Delivery_boy.Name,
                'tomorrow_date': tomorrow_date.strftime('%Y-%m-%d'),
            },
            'customer_data_list': data_list,
        })



#====================================================================================================
  ############################     CREATED  TRIP VIEW API        ##################################
    


class Trip_View(APIView):
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip, id=trip_id)
       
        customers = Customers.objects.filter(Cutomer_route=trip.Route_name, is_deleted=False, Current_status=1)
        data_list = []    

        for customer in customers:
            try:
                # Fetching the supply data for the given customer and trip date
                supply_entry = Supply.objects.get(Customer=customer, Supply_date=trip.Trip_date)
                total_given_bottle = supply_entry.Total_bottle
                milk_need = supply_entry.Today_bottle

            except Supply.DoesNotExist:
                total_given_bottle = 0

            # milk_need = calculate_bottle_Trip_View(customer, trip.Trip_date)

            data_list.append({
                'customer_id': customer.id,
                'customer_number': customer.Order_number,
                'name': customer.Nick_name,
                'nick_name': customer.N_name,
                'sequence_number': customer.get_latest_sequence_number(),
                'total_given_bottle': total_given_bottle,
                'milk_need_today': milk_need,
            })      

        return Response({
            'trip_data': {
                'trip_number': trip.Trip_number,
                'trip_date': trip.Trip_date,
                'route_name': trip.Route_name.Route_name,  
                'vehicle_number': trip.Vehicle_number.Vehicle_number, 
                'delivery_boy': trip.Delivery_boy.Name,
            },
            'customer_data_list': data_list,
        })
