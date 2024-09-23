from rest_framework import serializers
from ..models import UserWorkExperience

class UserWorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkExperience
        exclude = ['date_created', 'last_updated']