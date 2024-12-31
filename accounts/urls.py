# accounts/urls.py
from django.urls import path, include
from .views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView)
from .views import user_registration_view, UserRegistrationView, UserProfileView 

urlpatterns = [
    # Authentication Endpoints
    # path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # path('api-auth/', include("rest_framework.urls")),

    # Profile Management
    path('profile/', UserProfileView.as_view(), name='user_profile'),
        # Web-based registration
    path('register/', user_registration_view, name='user_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

