from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.trash.models import Trash, TrashRecord

@admin.register(Trash)
class TrashAdmin(ModelAdmin):
    list_display = ('name', 'location', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'location')

@admin.register(TrashRecord)
class TrashRecordAdmin(ModelAdmin):
    list_display = ('user', 'trash', 'weight', 'accepted_coin', 'status', 'created_at')
    list_filter = ('status', 'accepted_by')
    search_fields = ('user__username', 'trash__name')
    actions = ['verify_trash']

    @admin.action(description='Verifikasi dan terima sampah')
    def verify_trash(self, request, queryset):
        queryset.update(status='success')
