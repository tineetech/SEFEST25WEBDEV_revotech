from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User, UserProfile

@receiver(post_save, sender=User)
def create_user_profile_and_group(sender, instance, created, **kwargs):
    if created:
        # Buat UserProfile untuk user baru
        UserProfile.objects.create(user=instance)
        
        # Assign group berdasarkan role
        if instance.role == 'user':
            group, _ = Group.objects.get_or_create(name='User')
            instance.groups.add(group)
        elif instance.role == 'doctor':
            group, _ = Group.objects.get_or_create(name='Doctor')
            instance.groups.add(group)
        elif instance.role == 'admin':
            group, _ = Group.objects.get_or_create(name='Admin')
            instance.groups.add(group)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Memastikan profile selalu tersimpan
    if hasattr(instance, 'profile'):
        instance.profile.save()