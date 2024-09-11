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
from django.db.models import Avg, Count

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


################################averages####################################################


class GetAllAverageFreshChatInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {
                    "message": "No fresh chat insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_chat_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_interactions": round(
                fresh_chat_insights.values("actual_interactions").aggregate(
                    Avg("actual_interactions")
                )["actual_interactions__avg"],
                2,
            ),
            "average_handling_time": round(
                fresh_chat_insights.values("handling_time").aggregate(
                    Avg("handling_time")
                )["handling_time__avg"],
                2,
            ),
            "average_csat": round(
                fresh_chat_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_chat_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_chat_insights_stats = {
            "managed_by": managed_by,
            "total_male_agents": male_agents,
            "total_female_agents": female_agents,
            "total_agents": total_agents,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": average_stats,
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


class GetAllFreshChatInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(
        self, request, organisation_id, year, month, week, agent_type, *args, **kwargs
    ):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            month=month,
            week=week,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {
                    "message": "No fresh chat insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_chat_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_interactions": round(
                fresh_chat_insights.values("actual_interactions").aggregate(
                    Avg("actual_interactions")
                )["actual_interactions__avg"],
                2,
            ),
            "average_handling_time": round(
                fresh_chat_insights.values("handling_time").aggregate(
                    Avg("handling_time")
                )["handling_time__avg"],
                2,
            ),
            "average_csat": round(
                fresh_chat_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_chat_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_chat_insights_stats = {
            "Year": year,
            "managed_by": managed_by,
            "Month": month,
            "week": week,
            "agent_type": agent_type,
            "total_male_agents": male_agents,
            "total_female_agents": female_agents,
            "total_agents": total_agents,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": average_stats,
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


class GetAllFreshChatInsightsStatisticsWithoutWeekView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, year, month, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            month=month,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {
                    "message": "No fresh chat insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_chat_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_interactions": round(
                fresh_chat_insights.values("actual_interactions").aggregate(
                    Avg("actual_interactions")
                )["actual_interactions__avg"],
                2,
            ),
            "average_handling_time": round(
                fresh_chat_insights.values("handling_time").aggregate(
                    Avg("handling_time")
                )["handling_time__avg"],
                2,
            ),
            "average_csat": round(
                fresh_chat_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_chat_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_chat_insights_stats = {
            "Year": year,
            "managed_by": managed_by,
            "Month": month,
            "agent_type": agent_type,
            "total_male_agents": male_agents,
            "total_female_agents": female_agents,
            "total_agents": total_agents,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": average_stats,
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


class GetAllFreshChatInsightsStatisticsWithoutMonthAndWeekView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, year, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {
                    "message": "No fresh chat insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_chat_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_interactions": round(
                fresh_chat_insights.values("actual_interactions").aggregate(
                    Avg("actual_interactions")
                )["actual_interactions__avg"],
                2,
            ),
            "average_handling_time": round(
                fresh_chat_insights.values("handling_time").aggregate(
                    Avg("handling_time")
                )["handling_time__avg"],
                2,
            ),
            "average_csat": round(
                fresh_chat_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_chat_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_chat_insights_stats = {
            "Year": year,
            "managed_by": managed_by,
            "agent_type": agent_type,
            "total_male_agents": male_agents,
            "total_female_agents": female_agents,
            "total_agents": total_agents,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": average_stats,
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


####################################################
class NewGetAllFreshChatInsightsStatisticsWithWeekView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, year, month, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            month=month,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {
                    "message": "No fresh_chat insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_chat_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()

        weekly_average_stats = {}
        for week in range(1, 7):
            week_insights = fresh_chat_insights.filter(week=week)
            if week_insights.exists():
                weekly_average_stats[f"week {week}"] = {
                    "average_aes": round(
                        fresh_chat_insights.values("aes").aggregate(Avg("aes"))[
                            "aes__avg"
                        ],
                        2,
                    ),
                    "average_interactions": round(
                        fresh_chat_insights.values("actual_interactions").aggregate(
                            Avg("actual_interactions")
                        )["actual_interactions__avg"],
                        2,
                    ),
                    "average_handling_time": round(
                        fresh_chat_insights.values("handling_time").aggregate(
                            Avg("handling_time")
                        )["handling_time__avg"],
                        2,
                    ),
                    "average_csat": round(
                        fresh_chat_insights.values("csat").aggregate(Avg("csat"))[
                            "csat__avg"
                        ],
                        2,
                    ),
                    "average_overall_score": round(
                        fresh_chat_insights.values("overall_score").aggregate(
                            Avg("overall_score")
                        )["overall_score__avg"],
                        2,
                    ),
                }

            else:
                weekly_average_stats[f"week {week}"] = None

        all_fresh_chat_insights_stats = {
            "Year": year,
            "managed_by": managed_by,
            "Month": month,
            "agent_type": agent_type,
            "total_male_agents": male_agents,
            "total_female_agents": female_agents,
            "total_agents": total_agents,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": {
                "average_aes": round(
                    fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_interactions": round(
                    fresh_chat_insights.values("actual_interactions").aggregate(
                        Avg("actual_interactions")
                    )["actual_interactions__avg"],
                    2,
                ),
                "average_handling_time": round(
                    fresh_chat_insights.values("handling_time").aggregate(
                        Avg("handling_time")
                    )["handling_time__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_chat_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_chat_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
            "weekily_average_stats": weekly_average_stats,
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


class NewGetAllFreshChatInsightsStatisticsWithMonthView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, organisation_id, year, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {
                    "message": "No fresh_chat insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_chat_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_chat_insights.values_list("user_id", flat=True),
        ).count()

        monthly_average_stats = {}
        for month in [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]:
            month_insights = fresh_chat_insights.filter(month=month)
            if month_insights.exists():
                monthly_average_stats[month] = {
                    "average_aes": round(
                        fresh_chat_insights.values("aes").aggregate(Avg("aes"))[
                            "aes__avg"
                        ],
                        2,
                    ),
                    "average_interactions": round(
                        fresh_chat_insights.values("actual_interactions").aggregate(
                            Avg("actual_interactions")
                        )["actual_interactions__avg"],
                        2,
                    ),
                    "average_handling_time": round(
                        fresh_chat_insights.values("handling_time").aggregate(
                            Avg("handling_time")
                        )["handling_time__avg"],
                        2,
                    ),
                    "average_csat": round(
                        fresh_chat_insights.values("csat").aggregate(Avg("csat"))[
                            "csat__avg"
                        ],
                        2,
                    ),
                    "average_overall_score": round(
                        fresh_chat_insights.values("overall_score").aggregate(
                            Avg("overall_score")
                        )["overall_score__avg"],
                        2,
                    ),
                }

            else:
                monthly_average_stats[month] = None

        all_fresh_chat_insights_stats = {
            "Year": year,
            "managed_by": managed_by,
            "agent_type": agent_type,
            "total_male_agents": male_agents,
            "total_female_agents": female_agents,
            "total_agents": total_agents,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": {
                "average_aes": round(
                    fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_interactions": round(
                    fresh_chat_insights.values("actual_interactions").aggregate(
                        Avg("actual_interactions")
                    )["actual_interactions__avg"],
                    2,
                ),
                "average_handling_time": round(
                    fresh_chat_insights.values("handling_time").aggregate(
                        Avg("handling_time")
                    )["handling_time__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_chat_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_chat_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
            "monthly_average_stats": monthly_average_stats,
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


class GetUserMonthlyInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, user_id, year, month, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
            month=month,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {"message": "No fresh_chat insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )

        all_fresh_chat_insights_stats = {
            "Year": year,
            "Month": month,
            "managed_by": managed_by,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": {
                "average_aes": round(
                    fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_interactions": round(
                    fresh_chat_insights.values("actual_interactions").aggregate(
                        Avg("actual_interactions")
                    )["actual_interactions__avg"],
                    2,
                ),
                "average_handling_time": round(
                    fresh_chat_insights.values("handling_time").aggregate(
                        Avg("handling_time")
                    )["handling_time__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_chat_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_chat_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)


class GetUserYearlyInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshChatInsightsRetrieveSerializer
    queryset = FreshChatInsights.objects.all()

    def get(self, request, user_id, year, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_chat_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
        )

        if not fresh_chat_insights.exists():
            return Response(
                {"message": "No fresh_chat insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_chat_insights.first().managed_by
        grade_counts = fresh_chat_insights.values("grade").annotate(
            count=Count("grade")
        )

        all_fresh_chat_insights_stats = {
            "Year": year,
            "managed_by": managed_by,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": {
                "average_aes": round(
                    fresh_chat_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_interactions": round(
                    fresh_chat_insights.values("actual_interactions").aggregate(
                        Avg("actual_interactions")
                    )["actual_interactions__avg"],
                    2,
                ),
                "average_handling_time": round(
                    fresh_chat_insights.values("handling_time").aggregate(
                        Avg("handling_time")
                    )["handling_time__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_chat_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_chat_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
        }

        return Response(all_fresh_chat_insights_stats, status=status.HTTP_200_OK)
