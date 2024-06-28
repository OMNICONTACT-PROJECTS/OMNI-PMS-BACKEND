from django.db import models
from organisations.models import Organisation

class Department(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=False, null=False, related_name='omni_departments'),
    name = models.CharField(max_length=100, blank=False, null=False, help_text='This is the name of the department'),
    location = models.CharField(max_length=100, blank=True, null=True),

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True),
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True),

    def __str__(self):
        return self.name
