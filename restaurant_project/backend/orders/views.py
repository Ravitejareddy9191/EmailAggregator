import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from rest_framework import status
@api_view(['POST'])
def google_oauth_login(request):
    token = request.data.get('credentials')
    if not token:
        return JsonResponse({'error': 'Missing token'}, stauts=400)

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "361799545263-b016bsotf6jmijjbqab3pjlha68g9ap7.apps.googleusercontent.com")

        email = idinfo.get('email')
        name = idinfo.get('name')

        return JsonResponse({'email': email, 'name': name})
    except ValueError:
        return JsonResponse({'error': 'Invalid token'}, status=400)
@csrf_exempt
def oauth_login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                "361799545263-b016bsotf6jmijjbqab3pjlha68g9ap7.apps.googleusercontent.com"
            )

            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            user, created = User.objects.get_or_create(username=email, defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })

            login(request, user)
            return JsonResponse({'message': 'OAuth login successful'})

        except Exception as e:
            return JsonResponse({'error': 'OAuth verification failed'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
def order_list(request):
    orders = Order.objects.all().values()
    return JsonResponse(list(orders), safe=False)
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')
@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # later change to 'dashboard'
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
def dashboard_view(request):
    orders = Order.objects.all().order_by('-email_date')
    return render(request, 'orders/dashboard.html', {'orders': orders})


