from django.db import models

from accounts.models import User
from departments.models import Department

# Create your models here.


class Pdp(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="users_pdp",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="department_pdp",
    )
    career_goals = models.TextField(null=True,blank=True,)
    career_journey = models.TextField(null=True,blank=True,)
    skills = models.TextField(null=True,blank=True,)
    opportunities = models.TextField(null=True,blank=True,)
    development_goals = models.TextField(null=True,blank=True,)
    feedback = models.TextField(null=True,blank=True,)
    secondment = models.TextField(null=True,blank=True,)
    work_life_balance = models.TextField(null=True,blank=True,)
    personal_goals = models.TextField(null=True,blank=True,)
    suggestions = models.TextField(null=True,blank=True,)
    career_expectations = models.TextField(null=True,blank=True,)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the pdp was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
       return f"{self.user.first_name} {self.user.last_name}"



class PdpReviewer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="user_pdp_reviewer",
    )
    pdp = models.ForeignKey(
        Pdp,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="pdp",
    )
    comment = models.TextField(null=True,blank=True,)
    reviewer_feedback = models.TextField(null=True,blank=True,)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the pdp review was made",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
