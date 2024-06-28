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
