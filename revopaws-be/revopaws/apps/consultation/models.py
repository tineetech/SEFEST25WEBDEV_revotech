from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.users.models import Doctor

# Model untuk konsultasi antara user dan dokter
class Consultation(models.Model):
    CONSULTATION_TYPE_CHOICES = [
        ('chat', _('Chat')),
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
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

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
