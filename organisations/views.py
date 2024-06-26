from .serializers import OrganisationSerializer, OrganisationRetrieveSerializer
from .models import Organisation
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.


class CreateOrganisationView(CreateAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Organisation created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Organisation, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Organisation. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllOrganisations(ListAPIView):
    permission_classes = []
    serializer_class = OrganisationRetrieveSerializer
    queryset = Organisation.objects.all()


class OrganisationReadUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = OrganisationRetrieveSerializer
    queryset = Organisation.objects.all()
