from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organisation
from .organisation_number import generate_organisation_number


@receiver(post_save, sender=Organisation)
def update_organisation_number(sender, instance, created, **kwargs):
    if created:
        # Generate the initial organisation_number on creation
        instance.organisation_number = generate_organisation_number(
            instance.organisation_code, str(instance.pk), 4, 3
        )
        instance.save()
