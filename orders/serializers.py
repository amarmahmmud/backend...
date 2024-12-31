# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual order items
    """
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'quantity', 
            'price_at_time', 'total_price'
        ]
    
    def get_total_price(self, obj):
        return obj.total_price()

class OrderSerializer(serializers.ModelSerializer):
    """
    Comprehensive Order Serializer
    """
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    payment_method = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 
            'status', 'total_amount', 'is_paid',
            'created_at', 'updated_at', 
            'shipping_address', 'shipping_method',
            'tracking_number', 'payment_method',
            'items'
        ]
        read_only_fields = [
            'order_number', 'customer', 
            'created_at', 'updated_at'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Order Creation
    """
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'shipping_address', 'shipping_method', 
            'payment_method', 'items'
        ]
    
    def create(self, validated_data):
        """
        Custom create method to handle order and order items
        """
        # Extract order items
        items_data = validated_data.pop('items')
        
        # Set customer to current user
        customer = self.context['request'].user
        
        # Calculate total amount
        total_amount = 0
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items
        order_items = []
        for item_data in items_data:
            product = item_data.get('product')
            quantity = item_data.get('quantity', 1)
            
            # Validate product availability
            if product.stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for product {product.name}"
                )
            
            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_time=product.price
            )
            
            # Update product stock
            product.stock_quantity -= quantity
            product.save()
            
            # Calculate total amount
            total_amount += order_item.total_price()
            order_items.append(order_item)
        
        # Update order total amount
        order.total_amount = total_amount
        order.save()
        
        return order
