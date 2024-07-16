from django.db import models
from accounts.models import User
from organisations.models import Organisation

# Create your models here.


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class SubscriberFile(models.Model):
    FILE_TYPE = (
        ("XLSX", "XLSX"),
        ("XLS", "XLS"),
        ("CSV", "CSV"),
        ("JSON", "JSON"),
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, blank=False, null=False
    )
    # campaign_name = models.CharField(max_length=150, blank=True, null=True)
    file_type = models.CharField(
        max_length=50, blank=False, null=False, choices=FILE_TYPE
    )
    is_upload_template = models.BooleanField(default=False, null=True, blank=True)
    file = models.FileField(upload_to="subscriber_files", blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)