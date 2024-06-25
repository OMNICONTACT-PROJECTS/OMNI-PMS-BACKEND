from django.db.models.signals import post_save
from django.dispatch import receiver
from .username import get_username
from accounts.models import User


@receiver(post_save, sender=User)
def user_save_handler(sender, instance, created, **kwargs):
    if created and instance.username is None:
        if instance.institution_id is None:
            instance.username = get_username()
            instance.save()
        else:
            instance.username = get_username(
                institution=instance.institution_id
            )
            instance.save()

# @receiver(post_save, sender=User)
# def update_username(sender, instance, created, **kwargs):
#     if created:
#         # Generate the initial username on creation
#         instance.username = get_username(instance.institution_code)
#         instance.save()
