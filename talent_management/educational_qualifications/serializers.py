from rest_framework import serializers
from ..models import EducationalQualification
from accounts.serializers import MinimizedUserSerializer


class UserEducationalQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalQualification
        exclude = ["date_created", "last_updated"]


class RetrieveUserEducationalQualificationSerializer(serializers.ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = EducationalQualification
        fields = "__all__"
