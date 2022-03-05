from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer, RegisterSerializer

User = get_user_model()

# Create your views here.
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user_obj = User.objects.filter(username=user).first()
        if user_obj and user_obj.check_password(password):
            token = Token.objects.filter(user=user_obj).first()
            if not token:
                # Token will create if there is no token, this if for backward compatibility
                token = Token.objects.create(user=user_obj)
            return Response({'token': token.key, 'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials'}, status.HTTP_401_UNAUTHORIZED)

class RegisterAPIView(GenericAPIView):
    """
    View for SignUp
    AnonPermission is making sure
    that only anonymous Registers
    """
    serializer_class = RegisterSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.validated_data
            data.pop('password')  # pass should not be in response
            user=User.objects.get(username=data['username'])
            token = Token.objects.filter(user=user).first()
            data.update({'token': token.key})
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)