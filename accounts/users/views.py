from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    GenericAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import User
from .serializers import (
    UserProfPicSerializer,
    UserProfPicRetrieveSerializer,
)
from accounts.serializers import RetrieveMinimizedUserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from organisations.models import Organisation


class GetAllUserView(ListAPIView):
    permission_classes = []
    serializer_class = RetrieveMinimizedUserSerializer
    queryset = User.objects.all()


class RetrieveDestroyUserView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = RetrieveMinimizedUserSerializer
    queryset = User.objects.all()


class UploadUserProfilePicView(UpdateAPIView):
    permission_classes = []
    serializer_class = UserProfPicSerializer
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser]


class GetAllUsersByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveMinimizedUserSerializer
    queryset = User.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"error": "Organisation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            users = User.objects.filter(organisation_id=organisation_id)
            serializer = self.serializer_class(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

class UsersGenderRatioByOrganisationIdView(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveMinimizedUserSerializer
    queryset = User.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response("Organisation not found", status=status.HTTP_404_NOT_FOUND)
        else:
            total_employees = self.queryset.filter(organisation_id=organisation_id).count()
            total_male_employees = self.queryset.filter(gender="MALE").count()
            total_female_employees = self.queryset.filter(gender="FEMALE").count()

            if total_male_employees <= 0 and total_female_employees <= 0:
                return Response(
                    data={
                        "male_employees": {"total": 0, "percentage": 0},
                        "female_employees": {"total": 0, "percentage": 0},
                    },
                    status=status.HTTP_200_OK,
                )

            male_percentage = float(
                (total_male_employees / (total_male_employees + total_female_employees)) * 100
            )
            female_percentage = float(
                (total_female_employees / (total_male_employees + total_female_employees)) * 100
            )

            data = (
                {
                    "total_employees": total_employees,
                    "male_employees": {
                        "total": total_male_employees,
                        "percentage": f"{male_percentage:.2f}",
                    },
                    "female_employees": {
                        "total": total_female_employees,
                        "percentage": f"{female_percentage:.2f}",
                    },
                },
            )

            return Response(data, status=status.HTTP_200_OK)