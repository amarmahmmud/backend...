# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    Handles user creation with additional validation
    """
    account_type = serializers.ChoiceField(choices=['customer', 'vendor'], write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name', 'password', 
            'confirm_password', 'phone_number', 'account_type'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
        }

    def create(self, validated_data):
        account_type = validated_data.pop('account_type')
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        if account_type == 'customer':
            user.is_customer = True
        elif account_type == 'vendor':
            user.is_seller = True
        user.save()
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information
    """
    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'profile_picture',
            'shipping_address'
        ]
        read_only_fields = ['email']
