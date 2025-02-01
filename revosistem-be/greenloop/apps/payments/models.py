from django.db import models
from apps.users.models import CustomUser

class PaymentOption(models.Model):
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

class SwapRecord(models.Model):
    STATUS_CHOICES = [
        ('failed', 'Failed'),
        ('warning', 'Warning'),
        ('pending', 'Pending'),
        ('success', 'Success')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coin = models.PositiveIntegerField()
    totals_swap = models.DecimalField(max_digits=10, decimal_places=2)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.coin} koin"
