from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.payments.models import PaymentOption, SwapRecord

@admin.register(PaymentOption)
class PaymentOptionAdmin(ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(SwapRecord)
class SwapRecordAdmin(ModelAdmin):
    list_display = ('user', 'coin', 'totals_swap', 'payment_option', 'status', 'created_at')
    list_filter = ('status', 'payment_option')
    search_fields = ('user__username',)
