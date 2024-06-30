from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import User


class AuditTrailUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "gender",
            "organisation",
        ]


class UserProfPicSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "profile_picture",
        ]


class UserProfPicRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_picture",
        ]
