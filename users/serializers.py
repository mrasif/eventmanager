from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    # Avoid displaying password as a text field
    password = serializers.CharField(max_length=100, style={'input_type': 'password'})

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def create(self, validated_data):
        """
        overriding to avoid storing raw text password
        """
        user = User.objects.create_user(**validated_data)
        # Token created to return on the time of sign up
        Token.objects.create(user=user)
        return user

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')