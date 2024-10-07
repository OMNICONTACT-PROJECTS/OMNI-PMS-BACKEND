from import_export import resources
from .models import Agent, User


class AgentResource(resources.ModelResource):
    class Meta:
        model = Agent
        fields = (
            "id",
            "organisation",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "role",
            "national_id",
            "dob",
            "department",
            "nationality",
            "province",
            "home_address",
            "job_title",
            "current_location",
            "user_status",
            "account_status",
            "contract_type",
            "contract_tenure",
            "agent_type",
        )

        skip_unchanged = False
        use_bulk = True
        report_skipped = False
