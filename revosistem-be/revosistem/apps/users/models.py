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

class UserItems(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    koin = models.PositiveIntegerField(default=0)
    total_penukaran_sampah = models.PositiveIntegerField(default=0)
    penarikan_uang = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.koin} koin"
