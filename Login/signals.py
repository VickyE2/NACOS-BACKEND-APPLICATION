from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BaseUser

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        BaseUser.objects.create(user=instance)
    else:
        base_user, created = BaseUser.objects.get_or_create(user=instance)
        base_user.save()