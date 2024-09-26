from django.db import models
from organisations.models import Organisation
from accounts.models import User

# Create your models here.


class VoiceInsights(models.Model):
    AGENT_TYPE = (
       ("VOICE_HVC", "VOICE HVC"),
       ("VOICE_LVC", "VOICE LVC"),
        
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
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )
    speed_to_answer = models.FloatField(
        null=True,
        blank=True,
        help_text="Speed to answer should be in seconds",
    )
    targeted_inbound_calls = models.FloatField(
        null=True,
        blank=True,
        help_text="This is Weekly Targeted inbound calls",
    )
    actual_inbound_calls = models.FloatField(
        null=True,
        blank=True,
        help_text="This is Weekly inbound calls achieved by the agent",
    )
    targeted_talktime = models.FloatField(blank=True, null=True)
    actual_talktime = models.FloatField(blank=True, null=True)
    outbound_target_calls = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the Weekly Outbound target calls",
    )
    actual_outbound_calls = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the Weekly Outbound calls achieved by the agent",
    )
    after_call_work = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the weekly after call work",
    )
    customer_complaint = models.FloatField(null=True, blank=True)
    csat = models.FloatField(
        null=True, blank=True, help_text="This is the weekly csat"
    )
    calc_aes = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated aes",
    )
    calc_speed_to_answer = models.FloatField(null=True, blank=True)
    calc_targeted_inbound_calls = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated targeted inbound calls",
    )
    calc_actual_inbound_calls = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated inbound calls achieved by the agent",
    )
    calc_targeted_talktime = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the weekly calculated calculated targeted talktime",
    )
    calc_outbound_target = models.FloatField(null=True, blank=True)
    actual_calc_outbound_calls = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the Weekly calculated Outbound calls achieved by the agent",
    )
    calc_after_call_work = models.FloatField(null=True, blank=True)
    calc_customer_complaint = models.FloatField(
        null=True,
        blank=True,
    )
    calc_csat = models.FloatField(null=True, blank=True)

    weighted_aes = models.FloatField(null=False, blank=False)
    weighted_speed_to_answer = models.FloatField(null=True, blank=True)
    weighted_targeted_inbound_calls = models.FloatField(null=True, blank=True)
    weighted_actual_inbound_calls = models.FloatField(null=True, blank=True)
    weighted_targeted_talktime = models.FloatField(null=True, blank=True)
    weighted_actual_talktime = models.FloatField(null=True, blank=True)
    weighted_targeted_outbound = models.FloatField(null=True, blank=True)
    weighted_actual_outbound = models.FloatField(null=True, blank=True)
    weighted_after_call_work = models.FloatField(null=True, blank=True)
    weighted_customer_complaint = models.FloatField(null=True, blank=True)
    weighted_csat = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class CampaignInsightFile(models.Model):
    FILE_TYPE = (
        ("XLSX", "XLSX"),
        ("XLS", "XLS"),
        ("CSV", "CSV"),
        ("JSON", "JSON"),
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, blank=False, null=False
    )
    campaign_name = models.CharField(max_length=150, blank=True, null=True)
    file_type = models.CharField(
        max_length=50, blank=False, null=False, choices=FILE_TYPE
    )
    is_upload_template = models.BooleanField(default=False, null=True, blank=True)
    file = models.FileField(upload_to="voice_insights_files", blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.campaign_name}.{self.file_type}"


class FollowUpInsights(models.Model):
    AGENT_TYPE = (
        
        ("FOLLOWUP_AGENT", "FOLLOWUP AGENT"),
        
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
        related_name="user_follow_up_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )
    outbound = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the Weekly Outbound calls achieved by the agent",
    )
    csat = models.FloatField(null=True, blank=True, help_text="This is the weekly csat")
    calc_aes = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated aes",
    )
    calc_outbound = models.FloatField(
        null=True,
        blank=True,
        help_text="This is the Weekly calculated Outbound calls achieved by the agent",
    )
    calc_csat = models.FloatField(null=True, blank=True)
    weighted_aes = models.FloatField(null=False, blank=False)
    weighted_outbound = models.FloatField(null=True, blank=True)
    weighted_csat = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class HigherLifeFoundationInsights(models.Model):
    AGENT_TYPE = (
        
        ("HLF_AGENT", "HLF AGENT"),
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
        related_name="user_higher_life_foundation_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )

    csat = models.FloatField(null=True, blank=True, help_text="This is the weekly csat")

    resolved_count = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    service_level = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )

    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class SasaiInsights(models.Model):
    AGENT_TYPE = (
        
        ("SASAI_AGENT", "SASAI AGENT"),
        
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
        related_name="user_sasai_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )

    csat = models.FloatField(null=True, blank=True, help_text="This is the weekly csat")

    resolved_count = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    service_level = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )

    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class FreshDeskInsights(models.Model):
    AGENT_TYPE = (
        
        ("FRESHDESK_AGENT", "FRESHDESK AGENT"),
        
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
        related_name="user_fresh_desk_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )
    resolved_count = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    complaints = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )

    csat = models.FloatField(null=True, blank=True, help_text="This is the weekly csat")

    calc_aes = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated aes",
    )
    calc_resolved_count = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated resolve count",
    )
    calc_complaints = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated complaints",
    )
    calc_csat = models.FloatField(null=True, blank=True)

    weighted_aes = models.FloatField(null=False, blank=False)
    weighted_resolved_count = models.FloatField(null=True, blank=True)
    weighted_complaints = models.FloatField(null=True, blank=True)
    weighted_csat = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class FreshChatInsights(models.Model):
    AGENT_TYPE = (
        
        ("FRESHCHAT_LVC", "FRESHCHAT LVC"),
        ("FRESHCHAT_HVC", "FRESHCHAT HVC"),
       
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
        related_name="user_fresh_chat_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )
    targeted_interactions = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    actual_interactions = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    login_time_variance = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    handling_time = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    customer_complaint = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )

    csat = models.FloatField(null=True, blank=True, help_text="This is the weekly csat")

    calc_aes = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated aes",
    )
    calc_targeted_interactions = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated targeted interactions",
    )
    calc_actual_interactions = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated actual interactions",
    )
    calc_login_time_variance = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated login time variance",
    )
    calc_handling_time = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated handling time",
    )
    calc_customer_complaint = models.FloatField(
        null=False,
        blank=False,
        help_text="This is the weekly calculated customer complaint",
    )
    calc_csat = models.FloatField(null=True, blank=True)

    weighted_aes = models.FloatField(null=False, blank=False)
    weighted_targeted_interactions = models.FloatField(null=True, blank=True)
    weighted_actual_interactions = models.FloatField(null=True, blank=True)
    weighted_login_time_variance = models.FloatField(null=True, blank=True)
    weighted_handling_time = models.FloatField(null=True, blank=True)
    weighted_customer_complaint = models.FloatField(null=True, blank=True)
    weighted_csat = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"


class YamuraiInsights(models.Model):
    AGENT_TYPE = (
       
        ("YAMURAI_AGENT", "YAMURAI AGENT"),
        
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
        related_name="user_yamurai_insights",
    )
    agent_type = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=AGENT_TYPE,
    )
    managed_by = models.CharField(max_length=150, blank=True, null=True)
    year = models.PositiveIntegerField(null=False, blank=False)
    month = models.CharField(max_length=50, null=False, blank=False)
    week = models.PositiveIntegerField(
        null=False, blank=False, help_text="week should be a number"
    )
    aes = models.FloatField(
        null=False,
        blank=False,
        help_text="Average Evaluation Score (AES)",
    )

    csat = models.FloatField(null=True, blank=True, help_text="This is the weekly csat")

    resolved_queries = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    calc_aes = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    calc_resolved_queries = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    calc_csat = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    weighted_aes = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    weighted_resolved_queries = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )
    weighted_csat = models.FloatField(
        null=False,
        blank=False,
        help_text="",
    )

    overall_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE)

    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} ({self.user.last_name}"
