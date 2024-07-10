from ..models import FreshChatInsights
from accounts.serializers import MinimizedUserSerializer
from rest_framework.serializers import ModelSerializer


class FreshChatInsightsSerializer(ModelSerializer):

    class Meta:
        model = FreshChatInsights
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


class FreshChatInsightsRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = FreshChatInsights
        fields = "__all__"


class FreshChatInsightsUpdateSerializer(ModelSerializer):

    class Meta:
        model = FreshChatInsights
        fields = "__all__"
