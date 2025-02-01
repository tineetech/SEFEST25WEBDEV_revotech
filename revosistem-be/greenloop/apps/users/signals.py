from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from apps.users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        default_group, _ = Group.objects.get_or_create(name='client')
        instance.groups.add(default_group)
