from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart, Profile


@receiver(post_save, sender=User)
def create_user_related(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_related(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
