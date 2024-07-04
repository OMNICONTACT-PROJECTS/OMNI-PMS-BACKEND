from import_export import resources
from ..models import YamuraiInsights


class YamuraiInsightsResource(resources.ModelResource):
    class Meta:
        model = YamuraiInsights
        import_id_fields = [
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "csat",
            "resolved_queries",
            "calc_aes",
            "calc_csat",
            "calc_resolved_queries",
            "weighted_aes",
            "weighted_csat",
            "weighted_resolved_queries",
            "overall_score",
            "grade",
        ]
        fields = (
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "csat",
            "resolved_queries",
            "calc_aes",
            "calc_csat",
            "calc_resolved_queries",
            "weighted_aes",
            "weighted_csat",
            "weighted_resolved_queries",
            "overall_score",
            "grade",
        )
        skip_unchanged = True
        use_bulk = True
        report_skipped = False
