from .serializers import (
    UserPersonalDocumentSerializer,
    RetrieveUserPersonalDocumentSerializer,
)
from ..models import UserPersonalDocument
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.models import User
from organisations.models import Organisation

# Create your views here.


class UserPersonalDocumentCreate(GenericAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                data = {
                    "message": "Document uploaded successfully",
                    "data": serializer.data,
                }
                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to upload document, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return (
                Response(
                    {
                        "message": "Failed to upload document, Exception error occurred.",
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                ),
            )


class GetAllUserDocsView(ListAPIView):
    permission_classes = []
    serializer_class = RetrieveUserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()


class UpdateUserDocsView(GenericAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()

    def put(self, request, pk):
        try:
            personal_doc = self.queryset.get(pk=pk)
        except UserPersonalDocument.DoesNotExist:
            return Response(
                data={"error": "User document not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(
                personal_doc, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDestroyUserDocsView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = RetrieveUserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()


class GetDocumentsByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            personal_docs = self.queryset.filter(pk=user_id)
            serializer = self.serializer_class(personal_docs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllDocumentsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()

    def get(self, request, organisation_id):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            personal_docs = self.queryset.filter(user__organisation_id=organisation_id)
            serializer = self.serializer_class(personal_docs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserPersonalDocumentUpdateGetDeleteByID(GenericAPIView):
    permission_classes = []
    serializer_class = RetrieveUserPersonalDocumentSerializer
    queryset = UserPersonalDocument.objects.all()

    def get(self, request, pk):
        try:
            personal_doc = self.queryset.get(pk=pk)
        except UserPersonalDocument.DoesNotExist:
            return Response(
                data={"error": "User document not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(personal_doc)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            personal_doc = self.queryset.get(pk=pk)
        except UserPersonalDocument.DoesNotExist:
            return Response(
                data={"error": "User document not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            personal_doc.delete()
            return Response(
                data={"message": "User document deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
