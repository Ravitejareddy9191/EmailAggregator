# restaurant_project/backend/orders/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile with email credentials"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gmail_credentials = models.TextField(null=True, blank=True)  # Store encrypted credentials
    is_email_connected = models.BooleanField(default=False)
    last_email_sync = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # Link to user
    email_date = models.CharField(max_length=255, null=True, blank=True)
    sender = models.CharField(max_length=255, null=True)
    Order_No = models.CharField(max_length=255, null=True, blank=True)
    Customer_Name = models.TextField(null=True, blank=True)
    Mobile_No = models.CharField(max_length=20, null=True, blank=True)
    Item_Details = models.TextField(null=True, blank=True)
    Item_Description = models.TextField(null=True, blank=True)
    Sub_Total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Delivery_Charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    GST = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Grand_Total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Pay_Mode = models.CharField(max_length=100, null=True, blank=True)
    Delivery_Date = models.CharField(max_length=255, null=True, blank=True)
    Station = models.CharField(max_length=100, null=True, blank=True)
    Train_No_Name = models.CharField(max_length=50, null=True, blank=True)
    Coach = models.CharField(max_length=50, null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    platform = models.CharField(max_length=50, null=True, blank=True)  # Track which platform
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.Order_No} - {self.Customer_Name}"