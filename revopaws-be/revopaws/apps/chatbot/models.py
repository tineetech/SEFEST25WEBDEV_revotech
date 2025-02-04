from django.db import models
from django.conf import settings

class ChatAI(models.Model):
    chat_ai_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_chats'
    )
    message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Chat {self.chat_ai_id} with {self.user.username}"
