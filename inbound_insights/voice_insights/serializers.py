from ..models import VoiceInsights, VoiceInsightsFile
from accounts.serializers import MinimizedUserSerializer
from organisations.serializers import MinimizedOrganisationSerializer
from rest_framework.serializers import ModelSerializer


class VoiceInsightsSerializer(ModelSerializer):

    class Meta:
        model = VoiceInsights
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


class VoiceInsightsRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = VoiceInsights
        fields = "__all__"


class VoiceInsightsUpdateSerializer(ModelSerializer):

    class Meta:
        model = VoiceInsights
        fields = "__all__"


class VoiceInsightsFileSerializer(ModelSerializer):
    class Meta:
        model = VoiceInsightsFile
        exclude = ("date_created", "last_updated", "is_upload_template")

        extra_kwargs = {
            "organisation": {"required": True},
            "file": {"required": True},
            "file_type": {"required": True},
        }


class VoiceInsightsFileRetrieveSerializer(ModelSerializer):
    organisation = MinimizedOrganisationSerializer()

    class Meta:
        model = VoiceInsightsFile
        fields = "__all__"
