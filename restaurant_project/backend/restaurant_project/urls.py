from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from orders import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', order_views.dashboard_view, name='dashboard'),
    path('auth/', include('dj_rest_auth.urls')),  # Login, logout, password reset
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # Signup
    path('api/orders/', include('orders.urls')),
]


