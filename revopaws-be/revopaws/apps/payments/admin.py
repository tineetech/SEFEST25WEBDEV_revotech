from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.payments.models import PaymentOption

@admin.register(PaymentOption)
class PaymentOptionAdmin(ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)
