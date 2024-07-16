from django.db import models

from accounts.models import User

# Create your models here.


class Pdp(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="users_voice_insights",
    )