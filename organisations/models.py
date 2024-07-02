from django.db import models
from .organisation_number import generate_organisation_number as x


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=200, blank=True, null=True)
    organisation_code = models.CharField(
        max_length=10, blank=True, default="GI", null=True
    )
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    organisation_address = models.TextField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(
        upload_to="organisation_logos",
        default="organisation_logos/default_logo.jpg",
        blank=True,
        null=True,
    )
    active = models.BooleanField(
        default=True, help_text="active is a boolean field, can either be Tue or False"
    )
    organisation_number = models.CharField(
        max_length=100, blank=True, null=True, unique=True
    )

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.organisation_name}"
