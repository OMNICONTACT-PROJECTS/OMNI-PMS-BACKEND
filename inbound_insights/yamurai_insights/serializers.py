from ..models import YamuraiInsights, CampaignInsightFile
from accounts.serializers import MinimizedUserSerializer
from organisations.serializers import MinimizedOrganisationSerializer
from rest_framework.serializers import ModelSerializer


class YamuraiInsightsSerializer(ModelSerializer):

    class Meta:
        model = YamuraiInsights
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": True},
            "agent_type": {"required": True},
            "year": {"required": True},
            "month": {"required": True},
            "week": {"required": True},
            "aes": {"required": True},
            "resolved_queries": {"required": True},
            "overall_score": {"required": True},
            "grade": {"required": True},
        }


class YamuraiInsightsRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = YamuraiInsights
        fields = "__all__"


class YamuraiInsightsUpdateSerializer(ModelSerializer):

    class Meta:
        model = YamuraiInsights
        fields = "__all__"
