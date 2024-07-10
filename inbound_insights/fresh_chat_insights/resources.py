from import_export import resources
from ..models import FreshChatInsights


class FreshChatInsightsResource(resources.ModelResource):
    class Meta:
        model = FreshChatInsights
        import_id_fields = [
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "targeted_interactions",
            "actual_interactions",
            "login_time_variance",
            "handling_time",
            "customer_complaint",
            "csat",
            "calc_aes",
            "calc_targeted_interactions",
            "calc_actual_interactions",
            "calc_login_time_variance",
            "calc_handling_time",
            "calc_customer_complaint",
            "calc_csat",
            "weighted_aes",
            "weighted_targeted_interactions",
            "weighted_actual_interactions",
            "weighted_login_time_variance",
            "weighted_handling_time",
            "weighted_customer_complaint",
            "weighted_csat",
            "overall_score",
            "grade",
        ]
        fields = (
            "id",
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "targeted_interactions",
            "actual_interactions",
            "login_time_variance",
            "handling_time",
            "customer_complaint",
            "csat",
            "calc_aes",
            "calc_targeted_interactions",
            "calc_actual_interactions",
            "calc_login_time_variance",
            "calc_handling_time",
            "calc_customer_complaint",
            "calc_csat",
            "weighted_aes",
            "weighted_targeted_interactions",
            "weighted_actual_interactions",
            "weighted_login_time_variance",
            "weighted_handling_time",
            "weighted_customer_complaint",
            "weighted_csat",
            "overall_score",
            "grade",
        )
        skip_unchanged = True
        use_bulk = True
        report_skipped = False
