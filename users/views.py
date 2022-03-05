from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import LoginSerializer

User = get_user_model()

# Create your views here.
class LoginApi(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user_obj = User.objects.filter(username=user).first()
        if user_obj and user_obj.check_password(password):
            token = Token.objects.filter(user=user_obj).first()
            if token:
                return Response({'token': token.key, 'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials'}, status.HTTP_401_UNAUTHORIZED)