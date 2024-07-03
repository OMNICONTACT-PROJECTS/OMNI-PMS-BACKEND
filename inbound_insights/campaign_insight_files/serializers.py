from ..models import CampaignInsightFile
from organisations.serializers import MinimizedOrganisationSerializer
from rest_framework.serializers import ModelSerializer


class CampaignInsightFileSerializer(ModelSerializer):
    class Meta:
        model = CampaignInsightFile
        exclude = ("date_created", "last_updated", "is_upload_template")

        extra_kwargs = {
            "organisation": {"required": True},
            "file": {"required": True},
            "file_type": {"required": True},
        }


class CampaignInsightFileRetrieveSerializer(ModelSerializer):
    organisation = MinimizedOrganisationSerializer()

    class Meta:
        model = CampaignInsightFile
        fields = "__all__"
