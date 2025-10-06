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
    
class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for the password reset request.
    """
    email = serializers.EmailField(required=True)

# --- ADD THIS NEW SERIALIZER ---
class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for the password reset confirmation.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    uidb64 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Ensure the two passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data