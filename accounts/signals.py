# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw'):
        return
    if created:
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance, role='student')
