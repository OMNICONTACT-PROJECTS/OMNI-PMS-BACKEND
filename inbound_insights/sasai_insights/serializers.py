from ..models import SasaiInsights, CampaignInsightFile
from accounts.serializers import MinimizedUserSerializer
from organisations.serializers import MinimizedOrganisationSerializer
from rest_framework.serializers import ModelSerializer


class SasaiInsightsSerializer(ModelSerializer):

    class Meta:
        model = SasaiInsights
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": True},
            "agent_type": {"required": True},
            "year": {"required": True},
            "month": {"required": True},
            "week": {"required": True},
            "aes": {"required": True},
            "resolved_count": {"required": True},
            "service_level": {"required": True},
            "overall_score": {"required": True},
            "grade": {"required": True},
        }


class SasaiInsightsRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = SasaiInsights
        fields = "__all__"


class SasaiInsightsUpdateSerializer(ModelSerializer):

    class Meta:
        model = SasaiInsights
        fields = "__all__"
