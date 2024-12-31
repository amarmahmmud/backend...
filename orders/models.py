from django.db import models
# orders/models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from accounts.models import CustomUser
from products.models import Product

class Order(models.Model):
    """
    Comprehensive Order Model
    Tracks customer orders with detailed status
    """
    class OrderStatus(models.TextChoices):
        PENDING = 'PE', 'Pending'
        PROCESSING = 'PR', 'Processing'
        SHIPPED = 'SH', 'Shipped'
        DELIVERED = 'DE', 'Delivered'
        CANCELLED = 'CA', 'Cancelled'
        REFUNDED = 'RF', 'Refunded'
    
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CC', 'Credit Card'
        DEBIT_CARD = 'DC', 'Debit Card'
        PAYPAL = 'PP', 'PayPal'
        STRIPE = 'ST', 'Stripe'
        COD = 'CD', 'Cash on Delivery'
    
    # Order Metadata
    customer = models.ForeignKey(
        CustomUser, 
        related_name='orders', 
        on_delete=models.CASCADE
    )
    order_number = models.CharField(
        max_length=50, 
        unique=True
    )
    
    # Order Status
    status = models.CharField(
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    
    # Payment Information
    payment_method = models.CharField(
        max_length=2,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CREDIT_CARD
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_paid = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Shipping Information
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    
    def save(self, *args, **kwargs):
        """
        Generate unique order number if not provided
        """
        if not self.order_number:
            self.order_number = f'ORDER-{timezone.now().strftime("%Y%m%d")}-{self.customer.id}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Order {self.order_number} - {self.customer.email}'

class OrderItem(models.Model):
    """
    Detailed Order Item Model
    Tracks individual products within an order
    """
    order = models.ForeignKey(
        Order, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        related_name='order_items', 
        on_delete=models.PROTECT
    )
    
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price_at_time = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    def total_price(self):
        """
        Calculate total price for this order item
        """
        return self.quantity * self.price_at_time
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
