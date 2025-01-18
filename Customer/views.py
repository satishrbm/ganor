
from rest_framework import generics
from .models import*
from Customer.serializers import *
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework import status
from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from Route.serializers import RouteSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Customers
from django.views.decorators.csrf import csrf_exempt
import json


#=====================================================================================================@api_view(['GET'])
def get_order_number(request):
    last_order_number = Customers.objects.aggregate(Max('Order_number'))['Order_number__max']

    if last_order_number is not None:
        new_number = last_order_number + 1
        order_number = '0{:04d}'.format(new_number)  # Format the new number with leading zeros and prefix
    else:
        order_number = '00001'  # First order number

    # Assuming you have an OrderNumberSerializer defined
    serializer = OrderNumberSerializer({'order_number': order_number})
    data = serializer.data

    response = Response(data)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {}

    return response

#=====================================================================================================


# class CustomerCreateView(CreateAPIView):
#     queryset = Customers.objects.all()
#     serializer_class = AddCustomerSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)

#             return Response({'message': 'Customer created successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             error_messages = {'errors': serializer.errors}
#             return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)
        
#===============================================================================================

class CustomerCreateView(CreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = AddCustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_number = self.get_unique_order_number()
            serializer.validated_data['Order_number'] = order_number
            
            self.perform_create(serializer)
            return Response({'message': 'Customer created successfully'}, status=status.HTTP_201_CREATED)
        else:
            error_messages = {'errors': serializer.errors}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)

    def get_unique_order_number(self):
        while True:
            order_number = self.generate_order_number()
            if not Customers.objects.filter(Order_number=order_number).exists():
                return order_number

    def generate_order_number(self):
        last_order_number = Customers.objects.aggregate(Max('Order_number'))['Order_number__max']

        if last_order_number is not None:
            new_number = last_order_number + 1
            order_number = '0{:04d}'.format(new_number)  # Format the new number with leading zeros and prefix
        else:
            order_number = '00001'  # First order number

        return order_number


#===============================================================================================
class CustomerCreateView1(APIView):
    def post(self, request, format=None):
        serializer = AddCustomerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  # Save the customer instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#=====================================================================================================

class CustomerListView(generics.ListAPIView):
    serializer_class = ListCustomerSerializer

    def get_queryset(self):        
        return Customers.objects.filter(is_deleted=False, Current_status=1)
    

class CloseCustomerListView(generics.ListAPIView):
    serializer_class = ListCustomerSerializer

    def get_queryset(self):        
        return Customers.objects.filter(is_deleted=False, Current_status=0)
#====================================================================================================

class CustomerRestartView(APIView):
    def put(self, request, pk):
        try:
            instance = Customers.objects.get(pk=pk)
        except Customers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Update the restarted_date field with the current date
        request.data['Restarted_date'] = date.today()
        
        serializer = ReStartCustomerSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDeleteView(generics.DestroyAPIView):
    queryset = Customers.objects.all()
    serializer_class = DeleteCustomerSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "Customer deleted successfully."},
            status=status.HTTP_200_OK)

#=================================================================================================

class CustomerUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Customers.objects.all()
    serializer_class = EditCustomerSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'success': True,
                'message': 'Customer updated successfully.',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

#========================================================================================================


class RouteListView(generics.ListAPIView):
    serializer_class = CustomerRouteSerializer

    def get_queryset(self):
        return Route.objects.filter(is_deleted=False)
    
#=========================================================================================================
class SequenceAPIView(APIView):
    def post(self, request):
        serializer = SequenceSerializer(data=request.data, many=True)

        if serializer.is_valid():
            for seq_data in serializer.validated_data:
                customer = seq_data['Customer']
                sequence_number = seq_data['Sequence_number']

                existing_sequence = Sequence.objects.filter(Customer=customer).first()

                if existing_sequence:
                    existing_sequence.Sequence_number = sequence_number
                    existing_sequence.save()
                else:
                    Sequence.objects.create(Customer=customer, Sequence_number=sequence_number)

            return Response({"message": "Sequences saved/updated successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BottleAPIView(APIView):
    def post(self, request):
        serializer = BottleCountSerializer(data=request.data, many=True)

        if serializer.is_valid():
            for seq_data in serializer.validated_data:
                id = seq_data['id']
                bottle_to_subtract = seq_data['Total_bottle']

                customer = Customers.objects.filter(id=id).first()

                if customer:
                    # Subtract the bottle count
                    customer.Total_bottle = max(0, customer.Total_bottle - bottle_to_subtract)
                    customer.save()
                else:
                    pass

            return Response({"message": "Bottle count updated successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def update_total_bottle(request):
    data = request.data

    serializer = CustomerUpdateSerializer(data=data, many=True)
    if serializer.is_valid():
        for item in serializer.validated_data:
            customer_id = item['customer_id']
            total_bottle_to_update = item['Total_bottle']

            try:
                customer = Customers.objects.get(id=customer_id)
                current_total_bottle = customer.Total_bottle
                if total_bottle_to_update <= current_total_bottle:
                    customer.Total_bottle -= total_bottle_to_update
                    customer.save()
                else:
                    return Response({"error": f"Total_bottle to update exceeds current Total_bottle for customer {customer_id}"}, status=status.HTTP_400_BAD_REQUEST)
            except Customers.DoesNotExist:
                return Response({"error": f"Customer with id {customer_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Total_bottle updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ==========================================Mobile App ===========================================

@csrf_exempt 
@api_view(['POST'])
def App_login_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Order_number = data.get('Order_number')
            Mobile_number1 = data.get('Mobile_number1')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

        try:
            customer = Customers.objects.get(
                Order_number=Order_number,
                Mobile_number1=Mobile_number1
            )
            return JsonResponse({'message': 'Success', 'Customer_name': customer.Customer_name,
                                 'Customer_number':customer.Order_number,'Customer_mobile':customer.Mobile_number1,'address':customer.Nick_name, 'Customer_id' : customer.id ,"status":200}, status=200)
        except Customers.DoesNotExist:
            return JsonResponse({'message': 'Customer not found','status':404}, status=404)

    return JsonResponse({'message': 'Invalid request method',status:400}, status=400)



class LandmarkCreateView(generics.CreateAPIView):
    queryset = Landmark.objects.all()
    serializer_class = LandmarkSerializer

    def create(self, request, *args, **kwargs):
        response = super(LandmarkCreateView, self).create(request, *args, **kwargs)
        response.data['message'] = 'Landmark created successfully.'
        return response


class LandmarkListView(generics.ListAPIView):
    queryset = Landmark.objects.all()
    serializer_class = LandmarkSerializer




@api_view(['DELETE'])
def delete_landmark2(request, pk):
    try:
        landmark = Landmark.objects.get(id=pk)
        landmark.delete()
        return Response({'message': 'Landmark deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Landmark.DoesNotExist:
        return Response({'error': 'Landmark not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'An error occurred while deleting the landmark: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['DELETE'])
def delete_landmark(request, pk):
    try:
        landmark = Landmark.objects.get(id=pk)
    except Landmark.DoesNotExist:
        return Response({"message": "Landmark not found"}, status=status.HTTP_404_NOT_FOUND)

    landmark.delete()
    return Response({"message": "Landmark deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class CloseCustomerkListView(generics.ListAPIView):
    queryset = Close_customer.objects.all()
    serializer_class = CloseCustomerkListSerializer

    

@api_view(['POST'])
def create_close_customer(request):
    if request.method == 'POST':
        serializer = CloseCustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                'message': 'Record created successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class create_close_customer(generics.CreateAPIView):
#     queryset = Close_customer.objects.all()
#     serializer_class = CloseCustomerkSerializer

#     def create(self, request, *args, **kwargs):
#         response = super(create_close_customer, self).create(request, *args, **kwargs)
#         response.data['message'] = 'Record created successfully.'
#         return response

class create_close_customer(generics.CreateAPIView):
    queryset = Close_customer.objects.all()
    serializer_class = CloseCustomerSerializer

    def create(self, request, *args, **kwargs):
        # Call the parent class's create method to create the Close_customer record
        response = super(create_close_customer, self).create(request, *args, **kwargs)
        
        # Now, update the Customers table's Current_status field
        customer_id = response.data['Customers']  # Assuming your serializer returns the Customers id
        try:
            customer = Customers.objects.get(pk=customer_id)
            customer.Current_status = '0'
            customer.save()
        except Customers.DoesNotExist:
            pass  # Handle the case where the customer does not exist
        
        response.data['message'] = 'Record created successfully.'
        return response
    

###############################################################################################

                        # MOBILE APPLICATION #
###############################################################################################


from rest_framework import generics
from .models import User_delevery
from .serializers import UserDeleverySerializer

class UserDeleveryListCreateView(generics.ListCreateAPIView):
    queryset = User_delevery.objects.all()
    serializer_class = UserDeleverySerializer

class UserDeleveryCreateView(generics.CreateAPIView):
    queryset = User_delevery.objects.all()
    serializer_class = UserDeleverySerializer

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('Customers')
        date = request.data.get('Date')
        milk_needed = request.data.get('milk_need')

        existing_record = User_delevery.objects.filter(Customers=customer_id, Date=date).first()

        if existing_record:
            existing_record.milk_need = milk_needed
            existing_record.save()
            return Response(
                {
                    "message": "Record updated successfully",
                    "data": UserDeleverySerializer(existing_record).data
                },
                status=status.HTTP_200_OK
            )
        else:
            serializer = UserDeleverySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Record created successfully",
                        "data": serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "message": "Invalid data. Record not created or updated.",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
