from django.shortcuts import render
from rest_framework import generics
from .models import*
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from django.db.models import Max
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_order_number(request):
    last_order_number = Delivery_boy.objects.aggregate(Max('Code'))['Code__max']

    if last_order_number:
        last_number = int(last_order_number[1:])  # Remove the prefix and convert to integer
        new_number = last_number + 1
        order_number = '0{:04d}'.format(new_number)  # Format the new number with leading zeros and prefix
    else:
        order_number = '00001'  # First order number

    serializer = OrderNumberSerializer({'order_number': order_number})
    return Response(serializer.data)

class DeliveryboyCreateView(CreateAPIView):
    queryset = Delivery_boy.objects.all()
    serializer_class = Delivery_boySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'Delivery boy created successfully'}, status=status.HTTP_201_CREATED)
        else:
            error_messages = {'errors': serializer.errors}
            return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)


class DeliveryboyListView(generics.ListAPIView):
    serializer_class = Delivery_boyListSerializer

    def get_queryset(self):
        return Delivery_boy.objects.filter(is_deleted=False)



class DeliveryboyUpdateView(RetrieveUpdateAPIView):
    queryset = Delivery_boy.objects.all()
    serializer_class = Delivery_boySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'message': 'Delivery boy updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryboyDeleteView(generics.DestroyAPIView):
    queryset = Delivery_boy.objects.all()
    serializer_class = EditDelivery_boySerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"message": "Delivery boy deleted successfully."})