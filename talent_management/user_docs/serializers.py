from rest_framework import serializers
from ..models import UserPersonalDocument
from accounts.serializers import MinimizedUserSerializer


class UserPersonalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalDocument
        exclude = ["date_created", "last_updated"]


class RetrieveUserPersonalDocumentSerializer(serializers.ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = UserPersonalDocument
        fields = "__all__"
