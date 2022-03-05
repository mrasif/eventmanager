from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    # Avoid displaying password as a text field
    password = serializers.CharField(max_length=100, style={'input_type': 'password'})