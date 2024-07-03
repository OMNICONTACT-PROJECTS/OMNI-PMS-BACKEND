from rest_framework.serializers import ModelSerializer
from .models import Department
from rest_framework import serializers

from organisations.serializers import MinimizedOrganisationSerializer

class DepartmentSerializer(ModelSerializer):
    class Meta:
        model= Department
        fields= "__all__"
        extra_kwargs = {
            "organisation": {"required": True},
            "name": {"required": True},
        }

        

class DepartmentRetrieveSerializer(ModelSerializer):
    organisation = MinimizedOrganisationSerializer()
    class Meta:
        model= Department
        fields = '__all__'
        