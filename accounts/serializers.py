from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, UserBukUploadFile
from organisations.serializers import MinimizedOrganisationSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "role",
            "username",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "organisation": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "gender": {"required": True},
            "phone_number_1": {"required": True},
            "national_id": {"required": True},
            "nationality": {"required": True},
            "home_address": {"required": True},
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["organisation"] = user.organisation_id
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["role"] = user.role
        token["user_permission"] = (
            f"{[perm.codename for perm in user.user_permissions.all()]}"
        )

        return token


class RetrieveUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {"password": {"write_only": True}}


class RetrieveUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "firstName",
            "lastName",
            "middleNames",
            "gender",
            "altEmail",
            "phone_number_1",
        ]


class CheckOldPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs["id"]
        password = attrs["password"]

        return attrs


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


class RetrieveMinimizedUserSerializer(ModelSerializer):
    organisation = MinimizedOrganisationSerializer()

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {"password": {"write_only": True}}


class MinimizedUserSerializer(ModelSerializer):
    organisation = MinimizedOrganisationSerializer()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "organisation"]

        extra_kwargs = {"password": {"write_only": True}}


class UserBulkUploadFileSerializer(ModelSerializer):
    class Meta:
        model = UserBukUploadFile
        exclude = ("date_created", "last_updated")

        extra_kwargs = {
            "organisation": {"required": True},
            "file": {"required": True},
            "file_type": {"required": True},
        }


class UserBulkUploadFileRetrieveSerializer(ModelSerializer):
    organisation = MinimizedOrganisationSerializer()

    class Meta:
        model = UserBukUploadFile
        fields = "__all__"
