# In my understanding, signals are a means for decoupling modules. 
# Since your task seems to happen in only one module I'd customize save.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    We are using a singal here since we want to catch
    an event happend on an another model (User)
    """
    if created:
        Profile.objects.create(user=instance)