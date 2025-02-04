from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.users.models import User, UserProfile, Doctor

class Command(BaseCommand):
    help = 'Create default groups and permissions'

    def handle(self, *args, **options):
        
        user_group, user_created = Group.objects.get_or_create(name='User')
        doctor_group, doctor_created = Group.objects.get_or_create(name='Doctor')
        admin_group, admin_created = Group.objects.get_or_create(name='Admin')

        user_ct = ContentType.objects.get_for_model(User)
        profile_ct = ContentType.objects.get_for_model(UserProfile)
        doctor_ct = ContentType.objects.get_for_model(Doctor)

        user_permissions = [
            Permission.objects.get_or_create(
                codename='view_own_profile',
                name='Can view own profile',
                content_type=profile_ct,
            )[0],
            Permission.objects.get_or_create(
                codename='edit_own_profile',
                name='Can edit own profile',
                content_type=profile_ct,
            )[0],
        ]

        doctor_permissions = [
            Permission.objects.get_or_create(
                codename='view_own_doctor_profile',
                name='Can view own doctor profile',
                content_type=doctor_ct,
            )[0],
            Permission.objects.get_or_create(
                codename='edit_own_doctor_profile',
                name='Can edit own doctor profile',
                content_type=doctor_ct,
            )[0],
        ]

        user_group.permissions.set(user_permissions)
        doctor_group.permissions.set(doctor_permissions + user_permissions)
        
        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions')) 