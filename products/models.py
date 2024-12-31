from django.db import models
# products/models.py
from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser

class Category(models.Model):
    """
    Product Category Model
    Organizes products into hierarchical categories
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='children', 
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    """
    Product Brand Model
    Manages product manufacturers or brands
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to='brand_logos/', 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Comprehensive Product Model
    Covers detailed product information
    """
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    # Pricing and Inventory
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    
    # Relationships
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.SET_NULL,
        null=True
    )
    brand = models.ForeignKey(
        Brand, 
        related_name='products', 
        on_delete=models.SET_NULL,
        null=True
    )
    seller = models.ForeignKey(
        CustomUser, 
        related_name='products', 
        on_delete=models.CASCADE
    )
    
    # Product Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Product Variants and Options
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

class ProductImage(models.Model):
    """
    Product Image Model
    Supports multiple images per product
    """
    product = models.ForeignKey(
        Product, 
        related_name='images', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.name}"
