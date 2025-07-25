import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from UserApp.models import User
from django.utils import timezone
import json

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # ✅ Skip authentication untuk endpoint publik
        skip_urls = [
            '/api/user/auth/login/',
            '/api/user/auth/register/',
            '/admin/',
            '/api/user/auth/refresh/',  # Untuk refresh token
        ]
        
        # Skip jika URL dalam daftar skip
        if any(request.path.startswith(url) for url in skip_urls):
            return None
        
        # Skip jika method OPTIONS (CORS preflight)
        if request.method == 'OPTIONS':
            return None
        
        # ✅ Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return JsonResponse({
                'message': 'Authorization header required',
                'status': 401
            }, status=401)
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'message': 'Invalid authorization header format. Use: Bearer <token>',
                'status': 401
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        try:
            # ✅ Decrypt dan verify JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # ✅ Verify token belum expired
            current_time = timezone.now().timestamp()
            if payload.get('exp', 0) < current_time:
                return JsonResponse({
                    'message': 'Token has expired',
                    'status': 401
                }, status=401)
            
            # ✅ Get user dari database
            try:
                user = User.objects.get(id=payload['user_id'])
                
                # Cek apakah user masih aktif
                if not user.is_active:
                    return JsonResponse({
                        'message': 'Account is inactive',
                        'status': 403
                    }, status=403)
                
                # ✅ Attach user ke request object
                request.user = user
                request.token_payload = payload
                
            except User.DoesNotExist:
                return JsonResponse({
                    'message': 'User not found',
                    'status': 404
                }, status=404)
                
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'message': 'Token has expired',
                'status': 401
            }, status=401)
            
        except jwt.InvalidTokenError:
            return JsonResponse({
                'message': 'Invalid token',
                'status': 401
            }, status=401)
            
        except Exception as e:
            return JsonResponse({
                'message': 'Token verification failed',
                'error': str(e),
                'status': 401
            }, status=401)
        
        return None