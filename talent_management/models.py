from django.db import models
from accounts.models import User

# Create your models here.


class EducationalQualification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    institution_attended = models.CharField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=200, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    file = models.FileField(
        upload_to="user_educational_documents", blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserWorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    employer = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    job_description = models.TextField(max_length=500, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    reference_contact_1 = models.TextField(max_length=500, blank=True, null=True)
    reference_contact_2 = models.TextField(max_length=500, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserPersonalDocument(models.Model):
    user_PERSONAL_DOCUMENTS_TYPES = (
        ("RESUME", "RESUME"),
        ("CV", "CV"),
        ("IDENTIFICATION", "IDENTIFICATION"),
        ("EDUCATIONAL", "EDUCATIONAL"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    doc_type = models.CharField(
        max_length=200, blank=True, null=True, choices=user_PERSONAL_DOCUMENTS_TYPES
    )
    file = models.FileField(upload_to="user_documents", blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Promotion(models.Model):
    STATUS = (("CURRENT", "CURRENT"), ("PREVIOUS", "PREVIOUS"))
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    position = models.CharField(max_length=150, blank=False, null=False)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"