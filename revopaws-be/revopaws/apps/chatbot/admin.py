from django.contrib import admin
from .models import ChatAI
from unfold.admin import ModelAdmin

class ChatAIAdmin(ModelAdmin):
    list_display = ('chat_ai_id', 'user', 'timestamp')
    search_fields = ('user__username', 'message', 'ai_response')

admin.site.register(ChatAI, ChatAIAdmin)
