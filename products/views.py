from django.shortcuts import render
# products/views.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category, Brand
from .serializers import (
    ProductSerializer, 
    ProductCreateUpdateSerializer,
    CategorySerializer,
    BrandSerializer
)
from .permissions import IsSellerOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    """
    Comprehensive Product Management ViewSet
    Supports multiple operations with fine-grained permissions
    """
    # queryset = Product.objects.all()
    queryset = Product.objects.all().order_by('-created_at')  # Order by latest products
    permission_classes = [IsSellerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Filtering and Search Configuration
    filterset_fields = ['category', 'brand', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['GET'])
    def featured_products(self, request):
        """
        Custom action to retrieve featured products
        """
        featured_products = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['GET'])
    def active_vendor_products(self, request):
        """
        List products by active vendors, sorted by creation date (latest first)
        """
        products = self.get_queryset().filter(
            seller__is_active=True,
            is_active=True
        ).order_by('-created_at')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category Management ViewSet
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BrandViewSet(viewsets.ModelViewSet):
    """
    Brand Management ViewSet
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    