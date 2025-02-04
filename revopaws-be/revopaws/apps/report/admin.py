from django.contrib import admin
from .models import ReportQuestion
from unfold.admin import ModelAdmin

class ReportQuestionAdmin(ModelAdmin):
    list_display = ('report_id', 'user', 'subject', 'report_status', 'created_at', 'resolved_at')
    list_filter = ('report_status', 'created_at', 'resolved_at')

    search_fields = ('subject', 'user__username', 'user__email')

admin.site.register(ReportQuestion, ReportQuestionAdmin)
