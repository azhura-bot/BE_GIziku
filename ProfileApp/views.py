from django.shortcuts import render
from UserApp.models import User
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from UserApp.serializers import UserSerializer
from django.conf import settings
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfile(request):
    if request.method == 'GET':
        try:
            # Get token from Authorization header
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({
                    'message': 'Authorization token required',
                    'status': 401
                }, safe=False)
            
            token = auth_header.split(' ')[1]
            
            # Verify and decode JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if not user_id:
                return JsonResponse({
                    'message': 'Invalid token',
                    'status': 401
                }, safe=False)
            
            # Get user from database
            user = User.objects.get(id=user_id)
            # Use serializer to get all user data automatically
            serializer = UserSerializer(user)
            user_data = serializer.data            
            return JsonResponse({
                'message': 'Profile retrieved successfully',
                'data': user_data,
                'status': 200
            }, safe=False)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'message': 'Token has expired',
                'status': 401
            }, safe=False)
        except jwt.InvalidTokenError:
            return JsonResponse({
                'message': 'Invalid token',
                'status': 401
            }, safe=False)
        except User.DoesNotExist:
            return JsonResponse({
                'message': 'User not found',
                'status': 404
            }, safe=False)
        except Exception as e:
            return JsonResponse({
                'message': 'Failed to retrieve profile',
                'error': str(e),
                'status': 500
            }, safe=False)
    
    return JsonResponse({
        'message': 'Method not allowed',
        'status': 405
    }, safe=False)

@api_view(['PATCH', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def UpdateProfile(request):
    """
    Update user profile with support for both JSON data and file uploads.
    Fields are nullable - only provided fields will be updated.
    """
    # Debug incoming request
    print("\n=== REQUEST DEBUG ===")
    print("Method:", request.method)
    print("Content-Type:", request.headers.get('Content-Type'))
    print("Body Size:", len(request.body) if request.body else 0)
    print("FILES:", request.FILES)
    print("POST:", request.POST)
    print("=== END DEBUG ===\n")
    
    if request.method in ['PATCH', 'POST', 'PUT']:
        try:
            # Get and validate token
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({
                    'message': 'Authorization token required',
                    'status': 401
                }, safe=False)
            
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if not user_id:
                return JsonResponse({
                    'message': 'Invalid token - missing user_id',
                    'status': 401
                }, safe=False)
            
            # Get user
            user = User.objects.get(id=user_id)
            
            # Detect Content-Type
            content_type = request.headers.get('Content-Type', '').lower()
            
            # Create empty data dictionary for updates
            update_data = {}
            
            # HANDLE MULTIPART FORM DATA (with file upload)
            if 'multipart/form-data' in content_type or len(request.FILES) > 0:
                print("Processing multipart form data...")
                
                # Process text fields from POST
                for key, value in request.POST.items():
                    if key not in ['id', 'created_at', 'updated_at']:
                        update_data[key] = value
                
                # Process file upload if present
                if 'photo_profile' in request.FILES:
                    print("Photo profile found in request")
                    # We'll set this directly on the model instance later
                
            # HANDLE JSON DATA
            elif 'application/json' in content_type:
                print("Processing JSON data...")
                
                # Parse JSON
                if request.body:
                    json_data = JSONParser().parse(request)
                    
                    # Filter out restricted fields
                    for key, value in json_data.items():
                        if key not in ['id', 'created_at', 'updated_at']:
                            update_data[key] = value
                else:
                    print("Empty request body")
            
            # HANDLE URL-ENCODED FORM
            elif 'application/x-www-form-urlencoded' in content_type:
                print("Processing URL-encoded form data...")
                
                # Process form fields
                for key, value in request.POST.items():
                    if key not in ['id', 'unique_id', 'created_at', 'updated_at']:
                        update_data[key] = value
            
            # OTHER CONTENT TYPES
            else:
                print(f"Unsupported content type: {content_type}")
                # Try to parse as JSON anyway as fallback
                if request.body:
                    try:
                        json_data = JSONParser().parse(request)
                        for key, value in json_data.items():
                            if key not in ['id', 'unique_id', 'created_at', 'updated_at']:
                                update_data[key] = value
                    except Exception as e:
                        print(f"Failed to parse body: {str(e)}")
            
            # Check if we have any data to update
            print("Update data:", update_data)
            
            if not update_data and 'photo_profile' not in request.FILES:
                return JsonResponse({
                    'message': 'No data provided for update',
                    'status': 400
                }, safe=False)
            
            # Update user with collected data (supports partial update)
            serializer = UserSerializer(user, data=update_data, partial=True)
            
            if serializer.is_valid():
                print("Serializer is valid, saving...")
                # Save model without committing to database yet
                updated_user = serializer.save()
                
                # Handle file upload if present - outside of serializer
                if 'photo_profile' in request.FILES:
                    print("Saving photo profile...")
                    updated_user.photo_profile = request.FILES['photo_profile']
                    updated_user.save()
                
                # Get fresh serialized data
                serialized_data = UserSerializer(updated_user).data
                
                return JsonResponse({
                    'message': 'Profile updated successfully',
                    'data': serialized_data,
                    'status': 200
                }, safe=False)
            else:
                print("Serializer errors:", serializer.errors)
                return JsonResponse({
                    'message': 'Invalid data provided',
                    'errors': serializer.errors,
                    'status': 400
                }, safe=False)
                
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'message': 'Token has expired',
                'status': 401
            }, safe=False)
        except jwt.InvalidTokenError:
            return JsonResponse({
                'message': 'Invalid token format',
                'status': 401
            }, safe=False)
        except User.DoesNotExist:
            return JsonResponse({
                'message': 'User not found',
                'status': 404
            }, safe=False)
        except Exception as e:
            import traceback
            print("Exception in UpdateProfile:", str(e))
            print(traceback.format_exc())
            return JsonResponse({
                'message': 'Failed to update profile',
                'error': str(e),
                'status': 500
            }, safe=False)
    
    return JsonResponse({
        'message': 'Method not allowed',
        'status': 405
    }, safe=False)