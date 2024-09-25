from django.db import models
from accounts.models import User
from departments.models import Department

# Create your models here.


class Scorecard(models.Model):
    STATUS = (
        ("PENDING", "PENDING"),
        ("APPROVED", "APPROVED"),
        ("REVIEWED", "REVIEWED"),
    )

    name = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="scorecard_user",
    )
    actual_score = models.FloatField(null=True, blank=True)
    manager_score = models.FloatField(null=True, blank=True)
    document_proof = models.FileField(null=True, blank=True, upload_to="scorecard_docs")
    status = models.CharField(
        max_length=150, null=True, blank=True, default="PENDING", choices=STATUS
    )
    comment = models.TextField(
        null=True,
        blank=True,
    )
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.name}"


############################Key Focus Areas ###################################


class Strategy(models.Model):
    scorecard = models.ForeignKey(
        Scorecard, related_name="strategies", on_delete=models.CASCADE
    )
    strategic_objective = models.TextField(blank=True, null=True)
    performance_measure = models.TextField(blank=True, null=True)
    unit_measurement = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    fy_target = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    actual_score = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    variance = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    rating = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


class Customer(models.Model):
    scorecard = models.ForeignKey(
        Scorecard, related_name="customers", on_delete=models.CASCADE
    )
    strategic_objective = models.TextField(blank=True, null=True)
    performance_measure = models.TextField(blank=True, null=True)
    unit_measurement = models.TextField(blank=True, null=True)
    fy_target = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    weight = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    actual_score = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    variance = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    rating = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


class Innovation(models.Model):
    scorecard = models.ForeignKey(
        Scorecard, related_name="innovations", on_delete=models.CASCADE
    )
    strategic_objective = models.TextField(blank=True, null=True)
    performance_measure = models.TextField(blank=True, null=True)
    unit_measurement = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    fy_target = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    actual_score = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    variance = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    rating = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


class Function(models.Model):
    scorecard = models.ForeignKey(
        Scorecard, related_name="functions", on_delete=models.CASCADE
    )
    strategic_objective = models.TextField(blank=True, null=True)
    performance_measure = models.TextField(blank=True, null=True)
    unit_measurement = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    fy_target = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    actual_score = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    variance = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    rating = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


class Operation(models.Model):
    scorecard = models.ForeignKey(
        Scorecard, related_name="operations", on_delete=models.CASCADE
    )
    strategic_objective = models.TextField(blank=True, null=True)
    performance_measure = models.TextField(blank=True, null=True)
    unit_measurement = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    fy_target = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    actual_score = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    variance = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    rating = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard was created",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)


class ScorecardReview(models.Model):
    scorecard = models.ForeignKey(
        Scorecard,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="scorecard_review",
    )
    reviewer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="scorecard_reviewer",
    )
    initial_manager_comment = models.TextField(
        null=True,
        blank=True,
    )
    last_manager_comment = models.TextField(
        null=True,
        blank=True,
    )
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard review was made",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.scorecard.name}"


class ScorecardClone(models.Model):
    scorecard = models.ForeignKey(
        Scorecard,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="scorecard_clone",
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="scorecard_approver",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="scorecard_recipient",
    )
    date_created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
        help_text="The date the scorecard review was made",
    )
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.scorecard.name}"
