from .serializers import (
    VoiceInsightsSerializer,
    VoiceInsightsRetrieveSerializer,
    VoiceInsightsUpdateSerializer,
)
from ..campaign_insight_files.serializers import (
    CampaignInsightFileSerializer,
    CampaignInsightFileRetrieveSerializer,
)
from ..models import VoiceInsights, CampaignInsightFile
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
from .resources import VoiceInsightsResource
from rest_framework.parsers import MultiPartParser, FormParser
from tablib import Dataset
import pandas as pd
from django.db.models import Avg
# Create your views here.


class CreateVoiceInsightsView(CreateAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsSerializer
    queryset = VoiceInsights.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "VoiceInsights created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create voice insights, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Voice Insights. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllVoiceInsights(ListAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()


class VoiceInsightsReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()


class VoiceInsightsUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsUpdateSerializer
    queryset = VoiceInsights.objects.all()


class GetVoiceInsightsByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            voice_insights = self.queryset.filter(user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(voice_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetVoiceInsightsForHVCAgentsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            voice_insights = self.queryset.filter(agent_type="HVC").order_by(
                "-date_created"
            )
            serializer = self.serializer_class(voice_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetVoiceInsightsForLVCAgentsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            voice_insights = self.queryset.filter(agent_type="LVC").order_by(
                "-date_created"
            )
            serializer = self.serializer_class(voice_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetVoiceInsightsByGradeAndOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, grade, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            voice_insights = self.queryset.filter(
                user__organisation_id=organisation_id, grade=grade
            ).order_by("-date_created")
            serializer = self.serializer_class(voice_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetVoiceInsightsByDateAndOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, year, month, week, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            voice_insights = self.queryset.filter(
                user__organisation_id=organisation_id, year=year, month=month, week=week
            ).order_by("-date_created")
            serializer = self.serializer_class(voice_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class BulkUploadVoiceInsightsDataView(GenericAPIView):
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

                voice_insights_resource = VoiceInsightsResource()
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
                    result = voice_insights_resource.import_data(
                        dataset, dry_run=True, raise_errors=True
                    )
                except Exception as e:
                    error_message = str(e)
                    error_index = error_message.find("]")
                    if error_index != -1:
                        error_message = error_message[: error_index + 1]
                    return Response(
                        {
                            "message": "Failed to upload voice insights data, an error occurred",
                            "error": error_message,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not result.has_errors():
                    voice_insights_resource.import_data(dataset, dry_run=False)
                    try:
                        serializer = self.serializer_class(data=request.data)
                        if serializer.is_valid():
                            serializer.save()
                    except Exception as e:
                        pass
                    return Response(
                        {"message": "Voice Insights Data Uploaded Successfully."},
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
                        "message": "Failed to upload voice insights data, an error occurred",
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


class GetVoiceInsightsUploadedFilesView(GenericAPIView):
    permission_classes = []
    serializer_class = CampaignInsightFileSerializer
    queryset = CampaignInsightFile.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            voice_insights_files = self.queryset.filter(
                organisation_id=organisation_id
            ).order_by("-date_created")
            serializer = self.serializer_class(voice_insights_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UploadVoiceInsightsBulkUploadTemplate(GenericAPIView):
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
                "message": "Failed to upload voice insight template",
                "error": serializer.errors,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class GetVoiceInsightsBulkUploadTemplate(GenericAPIView):
    permission_classes = []
    serializer_class = CampaignInsightFileRetrieveSerializer
    queryset = CampaignInsightFile.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            voice_insights_files = self.queryset.filter(
                organisation_id=organisation_id, is_upload_template=True
            ).order_by("-date_created")
            serializer = self.serializer_class(voice_insights_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class GetAllAverageVoiceInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, organisation_id, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        voice_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
        )

        if not voice_insights.exists():
            return Response(
                {"message": "No voice insights data found for the given organisation"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        year= round(voice_insights.values("year").aggregate(Avg("year"))["year__avg"], 2),
        print("year is: ", year)

        average_stats = {
            "average_aes": round(voice_insights.values("weighted_aes").aggregate(Avg("weighted_aes"))["weighted_aes__avg"], 2),
            "average_outbound": round(voice_insights.values("weighted_actual_outbound").aggregate(Avg("weighted_actual_outbound"))["weighted_actual_outbound__avg"], 2),
            "average_talktime": round(voice_insights.values("weighted_actual_talktime").aggregate(Avg("weighted_actual_talktime"))["weighted_actual_talktime__avg"], 2),
            "average_inbound_calls": round(voice_insights.values("weighted_actual_inbound_calls").aggregate(Avg("weighted_actual_inbound_calls"))["weighted_actual_inbound_calls__avg"], 2),
            "average_csat": round(voice_insights.values("weighted_csat").aggregate(Avg("weighted_csat"))["weighted_csat__avg"], 2),
            "average_overall_score": round(voice_insights.values("overall_score").aggregate(Avg("overall_score"))["overall_score__avg"], 2),
        }

        return Response(average_stats, status=status.HTTP_200_OK)