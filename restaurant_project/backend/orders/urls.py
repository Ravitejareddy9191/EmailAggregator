from django.urls import path
from . import views
from .views import oauth_login_view, order_list, login_view, signup_view

urlpatterns = [
    path('', order_list, name='order-list'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name ='dashboard'),
    path('oauth/', oauth_login_view, name='oauth_login'),
    path('login/', login_view), 
]


