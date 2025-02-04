from django.contrib import admin
from .models import ChatRealtime
from unfold.admin import ModelAdmin

class ChatRealtimeAdmin(ModelAdmin):
    list_display = ('chat_id', 'user', 'doctor', 'message_type', 'timestamp')
    list_filter = ('message_type', 'timestamp')
    search_fields = ('user__username', 'doctor__name', 'message')

admin.site.register(ChatRealtime, ChatRealtimeAdmin)
