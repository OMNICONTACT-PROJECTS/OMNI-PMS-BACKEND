from django.db import models
from accounts.models import User

# Create your models here.


class Dev(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
