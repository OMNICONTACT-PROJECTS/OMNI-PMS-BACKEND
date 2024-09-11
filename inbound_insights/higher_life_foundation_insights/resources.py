from import_export import resources
from ..models import HigherLifeFoundationInsights


class HigherLifeFoundationInsightsResource(resources.ModelResource):
    class Meta:
        model = HigherLifeFoundationInsights
        import_id_fields = [
            "user",
            "agent_type",
            "year",
            "month",
            "week",
            "aes",
            "csat",
            "resolved_count",
            "service_level",
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
            "csat",
            "resolved_count",
            "service_level",
            "overall_score",
            "grade",
        )
        skip_unchanged = True
        use_bulk = True
        report_skipped = False
