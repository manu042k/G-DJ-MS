from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User objects"""
    password = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'email', 'phone_number', 'first_name', 'last_name', 
             'street_address', 'city', 'state', 
            'postal_code', 'country', 'password'
        ]

    def validate_password(self, value):
        """Check that the password meets the required criteria."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for JWT authentication."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['user_id'] = user.id
        return token

    