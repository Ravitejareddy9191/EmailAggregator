# restaurant_project/backend/orders/views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import Order, UserProfile
from .serializers import OrderSerializer

@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    """Handle user registration"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Validation
        if not all([username, email, password1, password2]):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        if password1 != password2:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return JsonResponse({'message': 'User created successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Handle user login"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def oauth_login_view(request):
    """Handle Google OAuth login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')

            if not token:
                return JsonResponse({'error': 'Token required'}, status=400)

            # Verify Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                "361799545263-b016bsotf6jmijjbqab3pjlha68g9ap7.apps.googleusercontent.com"
            )

            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            username = email.split('@')[0]  # Use email prefix as username

            # Create or get user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )

            # Create user profile if new user
            if created:
                UserProfile.objects.create(user=user)

            login(request, user)
            return JsonResponse({
                'message': 'OAuth login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })

        except Exception as e:
            return JsonResponse({'error': f'OAuth verification failed: {str(e)}'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})

@login_required
def order_list(request):
    """Get user-specific orders"""
    try:
        # Get orders for the authenticated user only
        orders = Order.objects.filter(user=request.user).values(
            'id', 'email_date', 'sender', 'Order_No', 'Customer_Name',
            'Mobile_No', 'Item_Details', 'Item_Description', 'Sub_Total',
            'Delivery_Charges', 'GST', 'Grand_Total', 'Pay_Mode',
            'Delivery_Date', 'Station', 'Train_No_Name', 'Coach', 
            'platform', 'created_at'
        )
        return JsonResponse(list(orders), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def dashboard_view(request):
    """Dashboard view for authenticated users"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/dashboard.html', {'orders': orders})

@login_required
def user_profile(request):
    """Get user profile information"""
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return JsonResponse({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name
            },
            'profile': {
                'is_email_connected': profile.is_email_connected,
                'last_email_sync': profile.last_email_sync
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def check_auth(request):
    """Check if user is authenticated"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email
        } if request.user.is_authenticated else None
    })