from django.db import models
from django.contrib.auth.models import AbstractUser
from organisations.models import Organisation


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
        ("SUBSCRIBER", "SUBSCRIBER"),
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
    # department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.CASCADE)
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
