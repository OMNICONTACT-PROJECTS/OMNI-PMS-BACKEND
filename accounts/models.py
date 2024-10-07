from django.db import models
from django.contrib.auth.models import AbstractUser
from organisations.models import Organisation
from departments.models import Department


class User(AbstractUser):
    # exclude fields from AbstractUser
    date_joined = None
    last_login = None
    email = None

    GENDER = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
    )
    ROLE = (
        ("DEV", "DEV"),
        ("SUPERUSER", "SUPERUSER"),
        ("ADMIN", "ADMIN"),
        ("AGENT", "AGENT"),
    )
    USER_STATUS = (
        ("ACTIVE", "ACTIVE"),
        ("ON_LEAVE", "ON_LEAVE"),
        ("ON_PAUSE", "ON_PAUSE"),
        ("BUFFER", "BUFFER"),
        ("SECONDMENT", "SECONDMENT"),
        ("TERMINATED", "TERMINATED"),
    )
    ACCOUNT_STATUS = (
        ("ACTIVE", "ACTIVE"),
        ("INACTIVE", "INACTIVE"),
    )
    CONTRACT_TYPE = (
        ("FIXED", "FIXED"),
        ("MNO", "MNO"),
        ("BUFFER", "BUFFER"),
    )
    AGENT_TYPE = (
        ("VOICE_HVC", "VOICE HVC"),
        ("VOICE_LVC", "VOICE LVC"),
        ("FOLLOWUP_AGENT", "FOLLOWUP AGENT"),
        ("FRESHDESK_AGENT", "FRESHDESK AGENT"),
        ("HLF_AGENT", "HLF AGENT"),
        ("SASAI_AGENT", "SASAI AGENT"),
        ("FRESHCHAT_LVC", "FRESHCHAT LVC"),
        ("FRESHCHAT_HVC", "FRESHCHAT HVC"),
        ("YAMURAI_AGENT", "YAMURAI AGENT"),
    )
    organisation = models.ForeignKey(
        Organisation, blank=True, null=True, on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    role = models.CharField(max_length=25, blank=True, null=True, choices=ROLE)
    gender = models.CharField(max_length=15, blank=True, null=True, choices=GENDER)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    home_address = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    current_location = models.CharField(max_length=155, blank=True, null=True)
    department = models.ForeignKey(
        Department, blank=True, null=True, on_delete=models.CASCADE
    )
    user_status = models.CharField(
        max_length=150, blank=True, null=True, choices=USER_STATUS
    )
    account_status = models.CharField(
        max_length=150, blank=True, null=True, choices=ACCOUNT_STATUS
    )
    contract_type = models.CharField(
        max_length=150, blank=True, null=True, choices=CONTRACT_TYPE
    )
    contract_tenure = models.CharField(max_length=20, blank=True, null=True)
    account_creation_date = models.DateField(auto_now_add=True, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="user_profile_pictures", blank=True, null=True
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )

    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the employee was enrolled on the organisation's system",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EducationalQualification(models.Model):
    QUALIFICATION_TYPE = (
        ("PHD", "PHD"),
        ("MASTERS", "MASTERS"),
        ("DEGREE", "DEGREE"),
        ("DIPLOMA", "DIPLOMA"),
        ("NATIONAL CERTIFICATE", "NATIONAL CERTIFICATE"),
        ("OTHER", "OTHER"),
    )
    EDUCATIONAL_LEVEL = (
        ("TERTIARY", "TERTIARY"),
        ("SECONDARY", "SECONDARY"),
        ("PRIMARY", "PRIMARY"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="educational_qualifications",
    )
    institution_attended = models.CharField(max_length=200, blank=True, null=True)
    qualification_type = models.CharField(
        max_length=200, blank=True, null=True, choices=QUALIFICATION_TYPE
    )
    educational_level = models.CharField(
        max_length=200, blank=True, null=True, choices=EDUCATIONAL_LEVEL
    )
    qualification = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    file = models.FileField(
        upload_to="users_educational_documents", blank=True, null=True
    )

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class UserPersonalDocument(models.Model):
    APPLICANT_PERSONAL_DOCUMENT_TYPE = (
        ("CV", "CV"),
        ("RESUME", "RESUME"),
        ("IDENTIFICATION", "IDENTIFICATION"),
        ("EDUCATIONAL", "EDUCATIONAL"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="personal_documents",
    )
    document_type = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=APPLICANT_PERSONAL_DOCUMENT_TYPE,
    )
    file = models.FileField(upload_to="applicant_documents", blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class UserBukUploadFile(models.Model):
    FILE_TYPE = (
        ("XLSX", "XLSX"),
        ("XLS", "XLS"),
        ("CSV", "CSV"),
        ("JSON", "JSON"),
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, blank=False, null=False
    )
    file_type = models.CharField(
        max_length=50, blank=False, null=False, choices=FILE_TYPE
    )
    file = models.FileField(upload_to="voice_insights_files", blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.file_type}"
