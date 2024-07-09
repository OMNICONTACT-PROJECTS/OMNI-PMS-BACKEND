from .serializers import (
    FreshChatInsightsSerializer,
    FreshChatInsightsRetrieveSerializer,
    FreshChatInsightsUpdateSerializer,
)
from ..campaign_insight_files.serializers import (
    CampaignInsightFileSerializer,
    CampaignInsightFileRetrieveSerializer,
)
from ..models import FreshChatInsights, CampaignInsightFile
from accounts.models import User
from organisations.models import Organisation
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework import status
from .resources import FreshChatInsightsResource
from rest_framework.parsers import MultiPartParser, FormParser
from tablib import Dataset
import pandas as pd

# Create your views here.


class CreateFreshChatInsightsView(CreateAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsSerializer
    queryset = FreshChatInsights.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Fresh Chat Insights created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Fresh Chat Insights, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Fresh Chat Insights. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllFreshChatInsights(ListAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()


class FreshChatInsightsReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()


class FreshChatInsightsUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsUpdateSerializer
    queryset = FreshChatInsights.objects.all()


class GetFreshChatInsightsByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            fresh_chat_insights = self.queryset.filter(user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(fresh_chat_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshChatInsightsForHVCAgentsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_chat_insights = self.queryset.filter(agent_type="HVC").order_by(
                "-date_created"
            )
            serializer = self.serializer_class(fresh_chat_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshChatInsightsForLVCAgentsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_chat_insights = self.queryset.filter(agent_type="LVC").order_by(
                "-date_created"
            )
            serializer = self.serializer_class(fresh_chat_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshChatInsightsByGradeAndOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, grade, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_chat_insights = self.queryset.filter(
                user__organisation_id=organisation_id, grade=grade
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_chat_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshChatInsightsByDateAndOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, year, month, week, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_chat_insights = self.queryset.filter(
                user__organisation_id=organisation_id, year=year, month=month, week=week
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_chat_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class BulkUploadFreshChatInsightsDataView(GenericAPIView):
    permission_classes = []
    serializer_class = CampaignInsightFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            Organisation.objects.get(pk=request.data.get("organisation"))
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            try:
                file_type = request.data.get("file_type", None)
                file = request.data.get("file", None)

                if not file_type or not file:
                    return Response(
                        {"error": "File type and file are required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                fresh_chat_insights_resource = FreshChatInsightsResource()
                df = None

                if file_type == "CSV":
                    try:
                        df = pd.read_csv(file)
                    except Exception as e:
                        return Response(
                            {
                                "error": "Failed to read the csv file, please check the file format."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                elif file_type == "json":
                    try:
                        df = pd.read_json(file)
                    except Exception as e:
                        return Response(
                            {
                                "error": "Failed to read the json file, please check the file format."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                elif file_type == "XLSX" or file_type == "XLS":
                    try:
                        df = pd.read_excel(file)
                    except Exception as e:
                        return Response(
                            {
                                "error": "Failed to read the excel file, please check the file format."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                else:
                    return Response(
                        {"error": "Unsupported file type."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                dataset = Dataset().load(df)
                try:
                    result = fresh_chat_insights_resource.import_data(
                        dataset, dry_run=True, raise_errors=True
                    )
                except Exception as e:
                    error_message = str(e)
                    error_index = error_message.find("]")
                    if error_index != -1:
                        error_message = error_message[: error_index + 1]
                    return Response(
                        {
                            "message": "Failed to upload fresh Chat insights data, an error occurred",
                            "error": error_message,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not result.has_errors():
                    fresh_chat_insights_resource.import_data(dataset, dry_run=False)
                    try:
                        serializer = self.serializer_class(data=request.data)
                        if serializer.is_valid():
                            saved_instance = serializer.save()
                            saved_instance.campaign_name = "Fresh Chat"
                            saved_instance.save()
                    except Exception as e:
                        pass
                    return Response(
                        {"message": "Fresh Chat Insights Data Uploaded Successfully."},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"error": "Error importing data."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                return Response(
                    {
                        "message": "Failed to upload fresh Chat insights data, an error occurred",
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


class GetFreshChatInsightsUploadedFilesView(GenericAPIView):
    permission_classes = []
    serializer_class = CampaignInsightFileSerializer
    queryset = CampaignInsightFile.objects.all()

    def get(self, request, organisation_id, campaign_name, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_chat_insights_files = self.queryset.filter(
                organisation_id=organisation_id, campaign_name=campaign_name
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_chat_insights_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UploadFreshChatInsightsBulkUploadTemplate(GenericAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CampaignInsightFileSerializer
    queryset = CampaignInsightFile.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CampaignInsightFileSerializer(data=request.data)
        if serializer.is_valid():
            saved_instance = serializer.save()
            saved_instance.is_upload_template = True
            saved_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Failed to upload fresh chat insight template",
                "error": serializer.errors,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class GetFreshChatInsightsBulkUploadTemplate(GenericAPIView):
    permission_classes = []
    serializer_class = CampaignInsightFileRetrieveSerializer
    queryset = CampaignInsightFile.objects.all()

    def get(self, request, organisation_id, campaign_name, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_chat_insights_files = self.queryset.filter(
                organisation_id=organisation_id,
                campaign_name=campaign_name,
                is_upload_template=True,
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_chat_insights_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
