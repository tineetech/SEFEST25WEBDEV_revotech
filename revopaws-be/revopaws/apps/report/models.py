from django.db import models
from django.conf import settings
from apps.ecommerce.models import Order

class ReportQuestion(models.Model):
    REPORT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='report_questions'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='report_questions'
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    report_status = models.CharField(
        max_length=10,
        choices=REPORT_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report by {self.user.username} - {self.subject}"
