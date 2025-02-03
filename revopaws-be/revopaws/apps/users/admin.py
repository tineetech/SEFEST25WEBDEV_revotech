from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from apps.users.models import CustomUser
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('username', 'email', 'membership', 'status', 'get_dashboard_link')
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

    def get_dashboard_link(self, obj):
        url = reverse('users_dashboard')
        return format_html(f'<a href="{url}" target="_blank">Lihat Dashboard Analytics</a>')
    get_dashboard_link.short_description = 'Dashboard Analytics'
