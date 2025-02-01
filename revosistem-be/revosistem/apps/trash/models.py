from django.db import models
from apps.users.models import CustomUser

class Trash(models.Model):
    STATUS_CHOICES = [
        ('closed', 'Closed'),
        ('verification', 'Verification'),
        ('available', 'Available')
    ]

    name = models.CharField(max_length=250)
    image = models.TextField()
    regency_name = models.CharField(max_length=250)
    district_name = models.CharField(max_length=250)
    village_name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    person_responsible = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TrashRecord(models.Model):
    STATUS_CHOICES = [
        ('failed', 'Failed'),
        ('warning', 'Warning'),
        ('pending', 'Pending'),
        ('success', 'Success')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trash = models.ForeignKey(Trash, on_delete=models.CASCADE)
    location = models.CharField(max_length=250, null=True, blank=True)
    image_proof = models.TextField()
    qty = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()  # in grams
    accepted_by = models.CharField(max_length=250, default='ai')
    accepted_coin = models.PositiveIntegerField()
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TrashRecord - {self.user.username} - {self.trash.name}"
