from django.shortcuts import render
# orders/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Order
from .serializers import (
    OrderSerializer, 
    OrderCreateSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Comprehensive Order Management ViewSet
    """
    queryset = Order.objects.all()
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    # Filtering and Search Configuration
    filterset_fields = [
        'status', 
        'is_paid', 
        'payment_method',
        'created_at'
    ]
    search_fields = [
        'order_number', 
        'shipping_address'
    ]
    ordering_fields = [
        'created_at', 
        'total_amount'
    ]
    
    def get_permissions(self):
        """
        Custom permissions based on action
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def get_serializer_class(self):
        """
        Use different serializers for different actions
        """
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        """
        Customize queryset based on user role
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)
    
    @action(detail=False, methods=['GET'])
    def recent_orders(self, request):
        """
        Retrieve recent orders for the current user
        """
        recent_orders = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(recent_orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PATCH'])
    def cancel_order(self, request, pk=None):
        """
        Allow order cancellation
        """
        order = self.get_object()
        
        # Check order cancellation eligibility
        if order.status not in [Order.OrderStatus.PENDING, Order.OrderStatus.PROCESSING]:
            return Response(
                {"error": "Order cannot be cancelled at this stage"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update order status
        order.status = Order.OrderStatus.CANCELLED
        order.save()
        
        # Restore product inventory
        for item in order.items.all():
            item.product.stock_quantity += item.quantity
            item.product.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
