from django.contrib import admin
from apps.users.models import User, UserProfile, Doctor
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
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
    list_display = ['name', 'specialization', 'str_number', 'verification_status']
