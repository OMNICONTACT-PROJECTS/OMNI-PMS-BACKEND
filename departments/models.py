from django.db import models
from organisations.models import Organisation


class Department(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, blank=False, null=True, related_name='department')
    name = models.CharField(max_length=200, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
