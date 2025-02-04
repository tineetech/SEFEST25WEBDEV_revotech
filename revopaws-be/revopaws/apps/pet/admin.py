from django.contrib import admin
from .models import Pet, PetMedicalRecord
from unfold.admin import ModelAdmin

class PetAdmin(ModelAdmin):
    list_display = ('pet_id', 'name', 'user', 'type', 'breed', 'birth_date', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'user__username', 'breed')

class PetMedicalRecordAdmin(ModelAdmin):
    list_display = ('record_id', 'pet', 'visit_date', 'diagnosis')
    list_filter = ('visit_date',)
    search_fields = ('pet__name', 'diagnosis', 'treatment')

admin.site.register(Pet, PetAdmin)
admin.site.register(PetMedicalRecord, PetMedicalRecordAdmin)
