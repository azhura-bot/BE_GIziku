from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import check_password
import jwt
import uuid
from django.utils import timezone
from django.conf import settings
# Models 
from UserApp.models import User
from UserApp.serializers import UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    if request.method == 'POST':
        try:
            user_request = JSONParser().parse(request)
            email = user_request.get('email')
            password = user_request.get('password')

            if not email or not password:
                return JsonResponse({
                    'message': 'Email and password are required',
                    'status': 400
                }, safe=False)

            # Gunakan serializer SimpleJWT
            serializer = TokenObtainPairSerializer(data={
                'email': email,
                'password': password
            })
            if serializer.is_valid():
                user = User.objects.get(email=email)
                user_data = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'is_active': user.is_active
                }
                return JsonResponse({
                    'message': 'Login successful',
                    'data': user_data,
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh'],
                    'token_type': 'Bearer',
                    'status': 200
                }, safe=False)
            else:
                return JsonResponse({
                    'message': 'Invalid credentials',
                    'errors': serializer.errors,
                    'status': 401
                }, safe=False)
        except Exception as e:
            return JsonResponse({
                'message': 'Login failed',
                'error': str(e),
                'status': 500
            }, safe=False)
    return JsonResponse({
        'message': 'Method not allowed',
        'status': 405
    }, safe=False)
     
@csrf_exempt
def Register(request):
    if request.method == 'POST':
        try:
            user_request = JSONParser().parse(request)
            
            # Ambil data yang diperlukan
            name = user_request.get('name')
            email = user_request.get('email')
            password = user_request.get('password')
            role = user_request.get('role', 'user')  # Default role is 'user'
            
            # Validasi input
            if not name or not email or not password:
                return JsonResponse({
                    'message': 'Name, email, and password are required',
                    'status': 400
                }, safe=False)
            
            # Cek apakah email sudah ada
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'message': 'Email already exists',
                    'status': 400
                }, safe=False)
            
            # Buat user baru
            user_data = {
                'name': name,
                'email': email,
                'password': password,
                'role': role
            }
            
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse({
                    'message': 'User registered successfully',
                    'data': {
                        'name': name,
                        'email': email,
                        'role': role
                    },
                    'status': 201
                }, safe=False)
            else:
                return JsonResponse({
                    'message': 'Invalid data',
                    'errors': user_serializer.errors,
                    'status': 400
                }, safe=False)
                
        except Exception as e:
            return JsonResponse({
                'message': 'Registration failed',
                'error': str(e),
                'status': 500
            }, safe=False)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def RefreshToken(request):
    if request.method == 'POST':
        try:
            user_request = JSONParser().parse(request)
            refresh_token = user_request.get('refresh')

            if not refresh_token:
                return JsonResponse({
                    'message': 'Refresh token required',
                    'status': 400
                }, safe=False)

            serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
            if serializer.is_valid():
                return JsonResponse({
                    'message': 'Token refreshed successfully',
                    'access': serializer.validated_data['access'],
                    'status': 200
                }, safe=False)
            else:
                return JsonResponse({
                    'message': 'Invalid refresh token',
                    'errors': serializer.errors,
                    'status': 401
                }, safe=False)
        except Exception as e:
            return JsonResponse({
                'message': 'Refresh failed',
                'error': str(e),
                'status': 500
            }, safe=False)
    return JsonResponse({
        'message': 'Method not allowed',
        'status': 405
    }, safe=False)