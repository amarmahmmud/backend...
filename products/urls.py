# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, BrandViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('active-vendor-products/', ProductViewSet.as_view({'get': 'active_vendor_products'}), name='active_vendor_products'),
]

# urlpatterns += [
#     path('active-vendor-products/', ProductViewSet.as_view({'get': 'active_vendor_products'}), name='active_vendor_products'),
# ]