from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.users.models import Doctor

# Model untuk konsultasi antara user dan dokter
class Consultation(models.Model):
    CONSULTATION_TYPE_CHOICES = [
        ('chat', _('Chat')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')), 
        ('paid', _('Paid')),       
        ('ongoing', _('Ongoing')), 
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled'))   
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('failed', _('Failed'))
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    consultation_type = models.CharField(max_length=10, choices=CONSULTATION_TYPE_CHOICES, default='chat')
    consultation_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    room_id = models.CharField(max_length=255, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Consultation with Dr. {self.doctor.user.username} on {self.consultation_date}"


# Model untuk review atau rating dari user kepada dokter
class DoctorReview(models.Model):
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='review'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_reviews'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for Dr. {self.doctor.user.username} (Rating: {self.rating})"


class ConsultationRoom(models.Model):
    ROOM_STATUS_CHOICES = [
        ('waiting', 'Waiting'),   
        ('active', 'Active'),     
        ('closed', 'Closed')      
    ]

    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='room'
    )
    room_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='waiting')
    doctor_joined_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room_id} - {self.get_status_display()}"

    @property
    def is_active(self):
        return self.status == 'active'