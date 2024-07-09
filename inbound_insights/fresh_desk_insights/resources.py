from import_export import resources
from ..models import FreshDeskInsights


class FreshDeskInsightsResource(resources.ModelResource):
    class Meta:
        model = FreshDeskInsights
        import_id_fields = [
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "resolved_count",
            "complaints",
            "csat",
            "calc_aes",
            "calc_resolved_count",
            "calc_complaints",
            "calc_csat",
            "weighted_aes",
            "weighted_resolved_count",
            "weighted_complaints",
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
            "resolved_count",
            "complaints",
            "csat",
            "calc_aes",
            "calc_resolved_count",
            "calc_complaints",
            "calc_csat",
            "weighted_aes",
            "weighted_resolved_count",
            "weighted_complaints",
            "weighted_csat",
            "overall_score",
            "grade",
        )
        skip_unchanged = True
        use_bulk = True
        report_skipped = False
