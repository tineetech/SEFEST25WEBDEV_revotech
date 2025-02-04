from django.contrib import admin
from .models import EducationalContent
from unfold.admin import ModelAdmin

class EducationalContentAdmin(ModelAdmin):
    list_display = ('content_id', 'title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

admin.site.register(EducationalContent, EducationalContentAdmin)
