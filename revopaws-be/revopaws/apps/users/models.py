from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):    
    MEMBERSHIP_CHOICES = [
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('exclusive', 'Exclusive')
    ]

    phone = models.CharField(max_length=20, null=True, blank=True)
    membership = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='starter')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}"