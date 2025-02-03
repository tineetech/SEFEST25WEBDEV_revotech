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
