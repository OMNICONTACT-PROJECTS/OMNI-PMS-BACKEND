from ..models import FreshDeskInsights, CampaignInsightFile
from accounts.serializers import MinimizedUserSerializer
from organisations.serializers import MinimizedOrganisationSerializer
from rest_framework.serializers import ModelSerializer


class FreshDeskInsightsSerializer(ModelSerializer):

    class Meta:
        model = FreshDeskInsights
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": True},
            "agent_type": {"required": True},
            "year": {"required": True},
            "month": {"required": True},
            "week": {"required": True},
            "aes": {"required": True},
            "calc_aes": {"required": True},
            "weighted_aes": {"required": True},
            "overall_score": {"required": True},
            "grade": {"required": True},
        }


class FreshDeskInsightsRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = FreshDeskInsights
        fields = "__all__"


class FreshDeskInsightsUpdateSerializer(ModelSerializer):

    class Meta:
        model = FreshDeskInsights
        fields = "__all__"
