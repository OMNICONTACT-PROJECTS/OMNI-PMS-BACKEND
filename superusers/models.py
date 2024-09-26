from django.db import models
from accounts.models import User

# Create your models here.


class Superuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the employee was enrolled on the organisation's system",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
