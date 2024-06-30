from django.db import models
from organisations.models import Organisation
from accounts.models import User

# Create your models here.


class VoiceInsights(models.Model):
    AGENT_TYPE = (
        ("LVC", "LVC"),
        ("HVC", "HVC"),
    )
    GRADE = (
        ("SP", "SP"),
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="users_voice_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.PositiveIntegerField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )
    speed_to_answer = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Speed to answer should be in seconds",
    )
    targeted_inbound_calls = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="This is Weekly Targeted inbound calls",
    )
    actual_inbound_calls = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="This is Weekly inbound calls achieved by the agent",
    )
    targeted_talktime = models.PositiveIntegerField(blank=True, null=True)
    actual_talktime = models.PositiveIntegerField(blank=True, null=True)
    outbound_target_calls = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="This is the Weekly Outbound target calls",
    )
    actual_outbound_calls = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="This is the Weekly Outbound calls achieved by the agent",
    )
    after_call_work = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="This is the weekly after call work",
    )
    customer_complaint = models.PositiveIntegerField(null=True, blank=True)
    csat = models.PositiveIntegerField(
        null=True, blank=True, help_text="This is the weekly csat"
    )
    calc_aes = models.PositiveIntegerField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated aes",
    )
    calc_speed_to_answer = models.PositiveIntegerField(null=True, blank=True)
    calc_targeted_inbound_calls = models.PositiveIntegerField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated targeted inbound calls",
    )
    calc_actual_inbound_calls = models.PositiveIntegerField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated inbound calls achieved by the agent",
    )
    calc_targeted_talktime = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        help_text="This is the weekly calculated calculated targeted talktime",
    )
    calc_outbound_target = models.PositiveIntegerField(null=True, blank=True)
    actual_calc_outbound_calls = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="This is the Weekly calculated Outbound calls achieved by the agent",
    )
    calc_after_call_work = models.PositiveIntegerField(null=True, blank=True)
    calc_customer_complaint = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    calc_csat = models.PositiveIntegerField(null=True, blank=True)

    weighted_aes = models.PositiveIntegerField(null=False, blank=False)
    weighted_speed_to_answer = models.PositiveIntegerField(null=True, blank=True)
    weighted_targeted_inbound_calls = models.PositiveIntegerField(null=True, blank=True)
    weighted_actual_inbound_calls = models.PositiveIntegerField(null=True, blank=True)
    weighted_targeted_talktime = models.PositiveIntegerField(null=True, blank=True)
    weighted_actual_talktime = models.PositiveIntegerField(null=True, blank=True)
    weighted_targeted_outbound = models.PositiveIntegerField(null=True, blank=True)
    weighted_actual_outbound = models.PositiveIntegerField(null=True, blank=True)
    weighted_after_call_work = models.PositiveIntegerField(null=True, blank=True)
    weighted_customer_complaint = models.PositiveIntegerField(null=True, blank=True)
    weighted_csat = models.PositiveIntegerField(null=True, blank=True)
    overall_score = models.PositiveIntegerField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class VoiceInsightsFile(models.Model):
    FILE_TYPE = (
        ("XLSX", "XLSX"),
        ("XLS", "XLS"),
        ("CSV", "CSV"),
        ("JSON", "JSON"),
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=False, null=False)
    file_type = models.CharField(
        max_length=50, blank=False, null=False, choices=FILE_TYPE
    )
    is_upload_template = models.BooleanField(default=False, null=True, blank=True)
    file = models.FileField(upload_to="voice_insights_files", blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.file_type}"
