from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "role", "username", "is_superuser", "is_staff", "is_active"]

        extra_kwargs = {'password': {'write_only': True},
                        "institution": {"required": True},
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

        token['institution'] = user.institution_id
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['role'] = user.role
        token['user_permission'] = f'{[perm.codename for perm in user.user_permissions.all()]}'

        return token


class RetrieveUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "password": {"write_only": True}
        }


class RetrieveUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'firstName',
            'lastName',
            'middleNames',
            'gender',
            'altEmail',
            'phone_number_1',
        ]


class CheckOldPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    password = serializers.CharField()

    def validate(self, attrs):
        # Validate the username and password.
        username = attrs['id']
        password = attrs['password']

        # Check if the username and password are correct.

        return attrs


class AuditTrailUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'gender',
            'institution',
        ]
