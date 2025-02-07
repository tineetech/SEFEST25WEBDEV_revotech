from django.db import models
from django.conf import settings
from apps.users.models import Doctor

class ChatRealtime(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    ]

    consultation = models.ForeignKey(
        'consultation.Consultation',
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    chat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='realtime_chats'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='realtime_chats'
    )
    message = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Untuk tracking pesan yang sudah dibaca

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Chat {self.chat_id} between {self.user.username} and Dr. {self.doctor.name}"
