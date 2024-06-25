from organisations.models import Organisation
from rest_framework.serializers import ModelSerializer


class OrganisationSerializer(ModelSerializer):

    class Meta:
        model = Organisation
        exclude = ['organisation_number']

        extra_kwargs = {
            "organisation_name": {"required": True},
            "organisation_code": {"required": True},
            "organisation_address": {"required": True},
            "phone_number": {"required": True},
        }


class OrganisationRetrieveSerializer(ModelSerializer):

    class Meta:
        model = Organisation
        fields = "__all__"

        
class MinimizedOrganisationSerializer(ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['id', 'organisation_name']