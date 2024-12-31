# products/serializers.py
from rest_framework import serializers
from .models import Product, Category, Brand, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'logo']

class ProductSerializer(serializers.ModelSerializer):
    """
    Comprehensive Product Serializer
    Includes nested serialization for related models
    """
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 
            'price', 'stock_quantity', 'category', 
            'brand', 'images', 'is_in_stock',
            'is_active', 'is_featured'
        ]

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Product Creation and Update
    Handles seller assignment and validation
    """
    images = ProductImageSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 
            'price', 'stock_quantity', 
            'category', 'brand', 'images',
            'is_active', 'is_featured'
        ]
    
    def create(self, validated_data):
        """
        Custom create method to handle product and images
        """
        # Remove images from validated data
        images_data = self.context.get('request').FILES.getlist('images')
        
        # Assign current user as seller
        validated_data['seller'] = self.context['request'].user
        
        # Create product
        product = Product.objects.create(**validated_data)
        
        # Create product images
        for image in images_data:
            ProductImage.objects.create(
                product=product, 
                image=image
            )
        
        return product
