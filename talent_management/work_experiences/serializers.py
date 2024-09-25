from rest_framework import serializers
from ..models import UserWorkExperience
from accounts.serializers import MinimizedUserSerializer


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkExperience
        exclude = ["date_created", "last_updated"]


class RetrieveUserWorkExperienceSerializer(serializers.ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = UserWorkExperience
        fields = "__all__"
