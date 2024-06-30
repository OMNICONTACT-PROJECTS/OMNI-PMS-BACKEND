from django.db.models.signals import post_save
from django.dispatch import receiver
from .username import get_username
from accounts.models import User


@receiver(post_save, sender=User)
def user_save_handler(sender, instance, created, **kwargs):
    if created and instance.username is None:
        instance.username = get_username(instance)
        instance.save()

    pass
