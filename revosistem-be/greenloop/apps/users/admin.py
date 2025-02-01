from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from apps.users.models import CustomUser, UserItems
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('username', 'email', 'membership', 'status')
    list_filter = ('membership', 'status')
    search_fields = ('username', 'email')
    
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = [
        ('User Info', {
            'fields': ['username', 'email', 'phone', 'membership', 'status', 'password']
        }),
        ('Permissions', {
            'fields': ['is_staff', 'is_superuser', 'groups', 'user_permissions']
        }),
    ]

@admin.register(UserItems)
class UserItemsAdmin(ModelAdmin):
    list_display = ('user', 'koin', 'total_penukaran_sampah', 'penarikan_uang')
    search_fields = ('user__username',)

