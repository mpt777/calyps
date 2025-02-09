from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status, routers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import  Response
from rest_framework.views import APIView
from .utils import get_tokens_for_user, get_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer
from django.urls import include, path, re_path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.authentication import JWTAuthentication

def get_user_from_token(token):
    try:
        jwt_authentication = JWTAuthentication()
        validated_token = jwt_authentication.get_validated_token(token)
        user = jwt_authentication.get_user(validated_token)
        return user
    except Exception as e:
        # Handle token validation errors
        return None

class CurrentUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # DRF automatically assigns the authenticated user
        if user.is_authenticated:
            return Response({"username": user.username, "email": user.email}, status=status.HTTP_200_OK)
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class RegistrationView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data, "message": "Registration successful"}, status=status.HTTP_201_CREATED)
        return Response({"message": "There are errors.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

      
class LoginView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        data = request.data 

        password = data.get('password', "")
        email = data.get('email', "")
        username = data.get('username', "")
        if not password or not (email or username):
          return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_user(email=email, username=username, password=password)

        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'message': 'Login Success', "user": {"username": user.username, "email": user.email}, **auth_data}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

      
class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully Logged out'}, status=status.HTTP_200_OK)


      
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


urlpatterns = [
  path('signup', RegistrationView.as_view(), name='signup'),
  path('current', CurrentUser.as_view(), name='current'),
  path('login', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('change-password', ChangePasswordView.as_view(), name='change_password'),
  path('token-refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]