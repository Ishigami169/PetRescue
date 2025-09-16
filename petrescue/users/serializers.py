# In users/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        # This list now correctly matches the fields in your User model
        fields = [
            'id', 'username', 'email', 'password', 'gender',
            'phone_no', 'address', 'pincode', 'profile_picture'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # Use the create_user helper to properly hash the password
        user = User.objects.create_user(**validated_data)
        return user