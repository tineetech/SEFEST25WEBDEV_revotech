from django.contrib import admin
from .models import PaymentLog
from unfold.admin import ModelAdmin

class PaymentLogAdmin(ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'user__username', 'user__email')

admin.site.register(PaymentLog, PaymentLogAdmin)
