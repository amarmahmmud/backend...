# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for admin interface
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form for admin interface
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
