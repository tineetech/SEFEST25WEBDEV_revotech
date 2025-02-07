from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

def doctor_directory_path(instance, filename):
    return f'doctor_{instance.user.id}/{filename}'

# Custom User
class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# UserProfile model (untuk user normal)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Doctor model relasi One-to-One ke User
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=255)
    photo_profile = models.ImageField(upload_to=doctor_directory_path, null=True, blank=True)
    str_number = models.CharField(max_length=50)
    chat_fee = models.DecimalField(max_digits=10, decimal_places=2)
    video_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    VERIFICATION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_CHOICES,
        default='pending'
    )
    specialization = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"