from import_export import resources
from .models import Agent, User


class AgentResource(resources.ModelResource):
    class Meta:
        model = Agent
        # import_id_fields = ('user')
        fields = (
            "user__organisation",
            "user__username",
            "user__first_name",
            "user__last_name",
            "user__email",
            "user__phone_number",
            "user__gender",
            "user__role",
            "user__national_id",
            "user__dob",
            "user__department",
            "user__nationality",
            "user__province",
            "user__home_address",
            "user__job_title",
            "user__current_location",
            "user__user_status",
            "user__account_status",
            "user__contract_type",
            "user__contract_tenure",
        )

        skip_unchanged = True
        use_bulk = True
        report_skipped = False
