from django.contrib import admin
from apps.users.models import User, UserProfile, Doctor
from unfold.admin import ModelAdmin

from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'role', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ['user', 'phone_number', 'birthday']

@admin.register(Doctor)
class DoctorAdmin(ModelAdmin):
    list_display = ['name', 'id', 'specialization', 'str_number', 'verification_status']
    list_filter = ['verification_status']
    actions = ['approve_doctors', 'reject_doctors']

    def approve_doctors(self, request, queryset):
        queryset.update(verification_status='approved')
    approve_doctors.short_description = "Approve selected doctors"

    def reject_doctors(self, request, queryset):
        queryset.update(verification_status='rejected')
    reject_doctors.short_description = "Reject selected doctors"
