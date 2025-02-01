from django.db import models
from apps.users.models import CustomUser

class ProductCategory(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active')
    ]

    name = models.CharField(max_length=250)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('hidden', 'Hidden')
    ]

    SHIPPING_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery')
    ]

    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    stock = models.PositiveIntegerField(default=0)
    price_cash = models.DecimalField(max_digits=10, decimal_places=2)
    price_coin = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    weight_in_grams = models.PositiveIntegerField()
    shipping_option = models.CharField(max_length=20, choices=SHIPPING_CHOICES, default='delivery')
    image_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('process', 'In Process'),
        ('being_sent', 'Being Sent'),
        ('ready_taken', 'Ready to Take'),
        ('success', 'Success')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    qty = models.PositiveIntegerField()
    product_cash = models.DecimalField(max_digits=10, decimal_places=2)
    product_coin = models.PositiveIntegerField()
    totals_cash = models.DecimalField(max_digits=10, decimal_places=2)
    totals_coin = models.PositiveIntegerField()
    shipping_option = models.CharField(max_length=20, choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], default='delivery')
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order - {self.product.name} - {self.buyer.username}"
