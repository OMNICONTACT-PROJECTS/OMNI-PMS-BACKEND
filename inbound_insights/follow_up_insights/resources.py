from import_export import resources
from ..models import FollowUpInsights


class FollowUpInsightsResource(resources.ModelResource):
    class Meta:
        model = FollowUpInsights
        import_id_fields = [
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "outbound",
            "csat",
            "calc_aes",
            "calc_outbound",
            "calc_csat",
            "weighted_aes",
            "weighted_outbound",
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
            "outbound",
            "csat",
            "calc_aes",
            "calc_outbound",
            "calc_csat",
            "weighted_aes",
            "weighted_outbound",
            "weighted_csat",
            "overall_score",
            "grade",
        )
        skip_unchanged = True
        use_bulk = True
        report_skipped = False
