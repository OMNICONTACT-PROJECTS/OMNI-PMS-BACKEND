from .serializers import UserWorkExperienceSerializer
from ..models import User, UserWorkExperience
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework import status

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
    serializer_class = UserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def get(self, request):
        experience = self.queryset.all()
        serializer = self.serializer_class(experience, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserWorkExperienceGetUpdateDeleteByID(GenericAPIView):
    permission_classes = []
    serializer_class = UserWorkExperienceSerializer
    queryset = UserWorkExperience.objects.all()

    def get(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(data={'error': 'User Work Experience not Found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(experience)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(data={'error': 'User Work Experience not Found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(experience, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.data,
                    "message": "User work experience created successfully"
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            experience = self.queryset.get(pk=pk)
        except UserWorkExperience.DoesNotExist:
            return Response(data={'error': 'User Work Experience not Found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            experience.delete()
            return Response(data={'message': 'User Work Experience deleted successfully.'},
                            status=status.HTTP_204_NO_CONTENT)