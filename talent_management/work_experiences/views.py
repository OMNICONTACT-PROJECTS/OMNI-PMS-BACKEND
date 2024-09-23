from .serializers import (
    UserWorkExperienceSerializer,
    RetrieveUserWorkExperienceSerializer,
)
from ..models import User, UserWorkExperience
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework import status
from organisations.models import Organisation

# Create your views here.


class UserWorkExperienceCreate(CreateAPIView):
    permission_classes = []
    serializer_class = UserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Work experience created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create work experience, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create work experience. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserWorkExperienceGetAll(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def get(self, request):
        experience = self.queryset.all()
        serializer = self.serializer_class(experience, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserWorkExperienceGetUpdateDeleteByID(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def get(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(
                data={"error": "User Work Experience not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(experience)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(
                data={"error": "User Work Experience not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(
                experience, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.data,
                    "message": "User work experience created successfully",
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(
                data={"error": "User Work Experience not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            experience.delete()
            return Response(
                data={"message": "User Work Experience deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )


class UpdateUserWorkExperienceGetUpdateDeleteByID(GenericAPIView):
    permission_classes = []
    serializer_class = UserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def put(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(
                data={"error": "User Work Experience not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(
                experience, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.data,
                    "message": "User work experience created successfully",
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetWorkExperienceByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def get(self, request, user_id):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            work_experience = self.queryset.filter(user_id=user_id)
            serializer = self.serializer_class(work_experience, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllWorkExperienceByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            work_experience = self.queryset.filter(
                user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(work_experience, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
