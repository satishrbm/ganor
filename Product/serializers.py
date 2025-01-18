from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['Product_name', 'Hsn_code', 'Product_unit', 'Product_price', 'Previous_stock', 'Minimum_stock',
                  'Maximum_stock', 'Product_active']

    def validate_Product_name(self, value):
        # Convert the product name to lowercase
        lowercase_name = value.lower()

        # Check if a product with the same lowercase name already exists
        if Product.objects.filter(Product_name__iexact=lowercase_name).exists():
            raise serializers.ValidationError("A product with this name already exists.")

        return value
    
    
class ProductSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['is_deleted']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','Product_name', 'Hsn_code', 'Product_unit', 'Product_price', 'Previous_stock', 'Minimum_stock',
                  'Maximum_stock', 'Product_active']

    def validate_Product_name(self, value):
        # Convert the product name to lowercase
        lowercase_name = value.lower()

        # Check if a product with the same lowercase name already exists
        if Product.objects.filter(Product_name__iexact=lowercase_name).exists():
            raise serializers.ValidationError("A product with this name already exists.")

        return value
    

class ProductEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['Product_name', 'Hsn_code', 'Product_unit', 'Product_price', 'Previous_stock', 'Minimum_stock',
                  'Maximum_stock', 'Product_active']