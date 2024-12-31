# .env File Template
"""
# Django Settings
SECRET_KEY=your_very_secret_and_long_random_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=ecommerce_db
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_SECRET_KEY=your_jwt_secret_key
"""

# ecommerce/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger Imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema Configuration
schema_view = get_schema_view(
   openapi.Info(
      title="E-Commerce API",
      default_version='v1',
      description="Comprehensive E-Commerce Platform API",
    #   terms_of_service="https://www.yourcompany.com/terms/",
    #   contact=openapi.Contact(email="contact@yourcompany.com"),
    #   license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin Site
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('accounts.urls')),
    
    # Product URLs
    path('api/products/', include('products.urls')),
    
    # Order URLs
    path('api/orders/', include('orders.urls')),
    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Additional Configuration Notes
"""
Key URL Routing Principles:
1. Modular URL configuration per app
2. API versioning support
3. Swagger documentation for API exploration
4. Separate routes for different resources
"""
