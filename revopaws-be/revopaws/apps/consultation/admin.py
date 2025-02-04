from django.contrib import admin
from .models import Consultation, DoctorReview
from unfold.admin import ModelAdmin

@admin.register(Consultation)
class ConsultationAdmin(ModelAdmin):
    list_display = ['user', 'doctor', 'consultation_type', 'consultation_date', 'payment_status', 'created_at']
    list_filter = ['consultation_type', 'payment_status']
    search_fields = ['user__username', 'doctor__user__username']

@admin.register(DoctorReview)
class DoctorReviewAdmin(ModelAdmin):
    list_display = ['user', 'doctor', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'doctor__user__username']
