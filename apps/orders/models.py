from django.db import models

# Create your models here.
# orders/models.py

from django.db import models
# from django.contrib.auth.models import User
from oauth.models import User
from product.models import Product  # assuming Product model is in `products` app
from address.models import Address  # assuming Shipping Address is in `addresses` app

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]
    
    CUSTOMER_STATUS_CHOICES = [
        ('PAYMENT_PENDING', 'Payment Pending'),
        ('ORDER_PLACED', 'Order Placed'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED_BY_USER', 'Cancelled by User'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.CharField(max_length=50, choices=CUSTOMER_STATUS_CHOICES, default='PAYMENT_PENDING')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    total_discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_items = models.PositiveIntegerField()

    sq_id_list = models.JSONField(default=list)  # list of sq_ids from products

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.email or self.user.mobile or self.user.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)  # optional, but common

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order #{self.order.id}"
