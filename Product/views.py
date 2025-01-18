from rest_framework import generics
from .models import*
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {
                    'success': True,
                    'message': 'Product created successfully.',
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

# class ProductUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductEditSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'Product_name' in serializer.validated_data and serializer.validated_data['Product_name'] != instance.Product_name:
            if Product.objects.filter(Product_name=serializer.validated_data['Product_name']).exclude(pk=instance.pk).exists():
                return Response({
                    'success': True,
                    'message': 'A product name already exists',
                }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Product updated successfully',
        }, status=status.HTTP_200_OK)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerDelete

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"message": "Product deleted successfully."})