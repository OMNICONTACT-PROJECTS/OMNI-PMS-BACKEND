from .serializers import (
    FreshDeskInsightsSerializer,
    FreshDeskInsightsRetrieveSerializer,
    FreshDeskInsightsUpdateSerializer,
)
from ..campaign_insight_files.serializers import (
    CampaignInsightFileSerializer,
    CampaignInsightFileRetrieveSerializer,
)
from ..models import FreshDeskInsights, CampaignInsightFile
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
from .resources import FreshDeskInsightsResource
from rest_framework.parsers import MultiPartParser, FormParser
from tablib import Dataset
import pandas as pd
from django.db.models import Avg, Count, Sum

# Create your views here.


class CreateFreshDeskInsightsView(CreateAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsSerializer
    queryset = FreshDeskInsights.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Fresh Desk Insights created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Fresh Desk Insights, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Fresh Desk Insights. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllFreshDeskInsights(ListAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()


class FreshDeskInsightsReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()


class FreshDeskInsightsUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsUpdateSerializer
    queryset = FreshDeskInsights.objects.all()


class GetFreshDeskInsightsByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            fresh_desk_insights = self.queryset.filter(user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(fresh_desk_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshDeskInsightsgentsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_desk_insights = self.queryset.order_by("-date_created")
            serializer = self.serializer_class(fresh_desk_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshDeskInsightsByGradeAndOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, grade, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_desk_insights = self.queryset.filter(
                user__organisation_id=organisation_id, grade=grade
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_desk_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetFreshDeskInsightsByDateAndOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, year, month, week, organisation_id, *args, **kwargs):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            fresh_desk_insights = self.queryset.filter(
                user__organisation_id=organisation_id, year=year, month=month, week=week
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_desk_insights, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class BulkUploadFreshDeskInsightsDataView(GenericAPIView):
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

                fresh_desk_insights_resource = FreshDeskInsightsResource()
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
                    result = fresh_desk_insights_resource.import_data(
                        dataset, dry_run=True, raise_errors=True
                    )
                except Exception as e:
                    error_message = str(e)
                    error_index = error_message.find("]")
                    if error_index != -1:
                        error_message = error_message[: error_index + 1]
                    return Response(
                        {
                            "message": "Failed to upload fresh desk insights data, an error occurred",
                            "error": error_message,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not result.has_errors():
                    fresh_desk_insights_resource.import_data(dataset, dry_run=False)
                    try:
                        serializer = self.serializer_class(data=request.data)
                        if serializer.is_valid():
                            saved_instance = serializer.save()
                            saved_instance.campaign_name = "Fresh Desk"
                            saved_instance.save()
                    except Exception as e:
                        pass
                    return Response(
                        {"message": "Fresh Desk Insights Data Uploaded Successfully."},
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
                        "message": "Failed to upload fresh desk insights data, an error occurred",
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


class GetFreshDeskInsightsUploadedFilesView(GenericAPIView):
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
            fresh_desk_insights_files = self.queryset.filter(
                organisation_id=organisation_id, campaign_name=campaign_name
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_desk_insights_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UploadFreshDeskInsightsBulkUploadTemplate(GenericAPIView):
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
                "message": "Failed to upload fresh desk insight template",
                "error": serializer.errors,
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class GetFreshDeskInsightsBulkUploadTemplate(GenericAPIView):
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
            fresh_desk_insights_files = self.queryset.filter(
                organisation_id=organisation_id,
                campaign_name=campaign_name,
                is_upload_template=True,
            ).order_by("-date_created")
            serializer = self.serializer_class(fresh_desk_insights_files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


####################Averages stats###############################################


class GetAllAverageFreshDeskInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {
                    "message": "No fresh desk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_desk_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_resolved_count": round(
                fresh_desk_insights.values("resolved_count").aggregate(
                    Avg("resolved_count")
                )["resolved_count__avg"],
                2,
            ),
            "average_complaints": round(
                fresh_desk_insights.values("complaints").aggregate(Avg("complaints"))[
                    "complaints__avg"
                ],
                2,
            ),
            "average_csat": round(
                fresh_desk_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_desk_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_desk_insights_stats = {
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

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class GetAllFreshDeskInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

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

        fresh_desk_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            month=month,
            week=week,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {
                    "message": "No fresh desk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_desk_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_resolved_count": round(
                fresh_desk_insights.values("resolved_count").aggregate(
                    Avg("resolved_count")
                )["resolved_count__avg"],
                2,
            ),
            "average_complaints": round(
                fresh_desk_insights.values("complaints").aggregate(Avg("complaints"))[
                    "complaints__avg"
                ],
                2,
            ),
            "average_csat": round(
                fresh_desk_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_desk_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_desk_insights_stats = {
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

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class GetAllFreshDeskInsightsStatisticsWithoutWeekView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, year, month, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            month=month,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {
                    "message": "No fresh desk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_desk_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_resolved_count": round(
                fresh_desk_insights.values("resolved_count").aggregate(
                    Avg("resolved_count")
                )["resolved_count__avg"],
                2,
            ),
            "average_complaints": round(
                fresh_desk_insights.values("complaints").aggregate(Avg("complaints"))[
                    "complaints__avg"
                ],
                2,
            ),
            "average_csat": round(
                fresh_desk_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_desk_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_desk_insights_stats = {
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

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class GetAllFreshDeskInsightsStatisticsWithoutMonthAndWeekView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, year, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {
                    "message": "No fresh desk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_desk_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()

        average_stats = {
            "average_aes": round(
                fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
            ),
            "average_resolved_count": round(
                fresh_desk_insights.values("resolved_count").aggregate(
                    Avg("resolved_count")
                )["resolved_count__avg"],
                2,
            ),
            "average_complaints": round(
                fresh_desk_insights.values("complaints").aggregate(Avg("complaints"))[
                    "complaints__avg"
                ],
                2,
            ),
            "average_csat": round(
                fresh_desk_insights.values("csat").aggregate(Avg("csat"))["csat__avg"],
                2,
            ),
            "average_overall_score": round(
                fresh_desk_insights.values("overall_score").aggregate(
                    Avg("overall_score")
                )["overall_score__avg"],
                2,
            ),
        }

        all_fresh_desk_insights_stats = {
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

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


####################################################
class NewGetAllFreshDeskInsightsStatisticsWithWeekView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, year, month, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            month=month,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {
                    "message": "No fresh_desk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_desk_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()

        weekly_average_stats = {}
        for week in range(1, 7):
            week_insights = fresh_desk_insights.filter(week=week)
            if week_insights.exists():
                weekly_average_stats[f"week {week}"] = {
                    "average_aes": round(
                        week_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
                    ),
                    "average_resolved_count": round(
                        week_insights.values("resolved_count").aggregate(
                            Avg("resolved_count")
                        )["resolved_count__avg"],
                        2,
                    ),
                    "average_complaints": round(
                        week_insights.values("complaints").aggregate(Avg("complaints"))[
                            "complaints__avg"
                        ],
                        2,
                    ),
                    "average_csat": round(
                        week_insights.values("csat").aggregate(Avg("csat"))[
                            "csat__avg"
                        ],
                        2,
                    ),
                    "average_overall_score": round(
                        week_insights.values("overall_score").aggregate(
                            Avg("overall_score")
                        )["overall_score__avg"],
                        2,
                    ),
                }

            else:
                weekly_average_stats[f"week {week}"] = None

        all_fresh_desk_insights_stats = {
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
                    fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_resolved_count": round(
                    fresh_desk_insights.values("resolved_count").aggregate(
                        Avg("resolved_count")
                    )["resolved_count__avg"],
                    2,
                ),
                "average_complaints": round(
                    fresh_desk_insights.values("complaints").aggregate(
                        Avg("complaints")
                    )["complaints__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_desk_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_desk_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
            "weekily_average_stats": weekly_average_stats,
        }

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class NewGetAllFreshDeskInsightsStatisticsWithMonthView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, year, agent_type, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {
                    "message": "No fresh_desk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )
        total_agents = (
            fresh_desk_insights.values("user_id")
            .annotate(count=Count("user_id"))
            .count()
        )

        male_agents = User.objects.filter(
            organisation=organisation,
            gender="MALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
        ).count()
        female_agents = User.objects.filter(
            organisation=organisation,
            gender="FEMALE",
            id__in=fresh_desk_insights.values_list("user_id", flat=True),
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
            month_insights = fresh_desk_insights.filter(month=month)
            if month_insights.exists():
                monthly_average_stats[month] = {
                    "average_aes": round(
                        month_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                        2,
                    ),
                    "average_resolved_count": round(
                        month_insights.values("resolved_count").aggregate(
                            Avg("resolved_count")
                        )["resolved_count__avg"],
                        2,
                    ),
                    "average_complaints": round(
                        month_insights.values("complaints").aggregate(
                            Avg("complaints")
                        )["complaints__avg"],
                        2,
                    ),
                    "average_csat": round(
                        month_insights.values("csat").aggregate(Avg("csat"))[
                            "csat__avg"
                        ],
                        2,
                    ),
                    "average_overall_score": round(
                        month_insights.values("overall_score").aggregate(
                            Avg("overall_score")
                        )["overall_score__avg"],
                        2,
                    ),
                }

            else:
                monthly_average_stats[month] = None

        all_fresh_desk_insights_stats = {
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
                    fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_resolved_count": round(
                    fresh_desk_insights.values("resolved_count").aggregate(
                        Avg("resolved_count")
                    )["resolved_count__avg"],
                    2,
                ),
                "average_complaints": round(
                    fresh_desk_insights.values("complaints").aggregate(
                        Avg("complaints")
                    )["complaints__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_desk_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_desk_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
            "monthly_average_stats": monthly_average_stats,
        }

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class GetUserMonthlyInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, user_id, year, month, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
            month=month,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {"message": "No fresh_desk insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )

        all_fresh_desk_insights_stats = {
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
                    fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_resolved_count": round(
                    fresh_desk_insights.values("resolved_count").aggregate(
                        Avg("resolved_count")
                    )["resolved_count__avg"],
                    2,
                ),
                "average_complaints": round(
                    fresh_desk_insights.values("complaints").aggregate(
                        Avg("complaints")
                    )["complaints__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_desk_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_desk_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
        }

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class GetUserYearlyInsightsStatisticsView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, user_id, year, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        fresh_desk_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
        )

        if not fresh_desk_insights.exists():
            return Response(
                {"message": "No fresh_desk insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = fresh_desk_insights.first().managed_by
        grade_counts = fresh_desk_insights.values("grade").annotate(
            count=Count("grade")
        )

        all_fresh_desk_insights_stats = {
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
                    fresh_desk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "average_resolved_count": round(
                    fresh_desk_insights.values("resolved_count").aggregate(
                        Avg("resolved_count")
                    )["resolved_count__avg"],
                    2,
                ),
                "average_complaints": round(
                    fresh_desk_insights.values("complaints").aggregate(
                        Avg("complaints")
                    )["complaints__avg"],
                    2,
                ),
                "average_csat": round(
                    fresh_desk_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "average_overall_score": round(
                    fresh_desk_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
        }

        return Response(all_fresh_desk_insights_stats, status=status.HTTP_200_OK)


class GetAllInsightsMonthlyStatisticsPerUserView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, organisation_id, agent_type, year, user_id, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        try:
            user= User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        freshDeskInsights = self.queryset.filter(
            user__organisation=organisation,
            agent_type=agent_type,
            year=year,
            user=user,
        )

        calendar_order = [
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
        ]
        
        if not freshDeskInsights.exists():
            return Response(
                {
                    "message": "No freshDesk insights data found for the given organisation"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        monthly_totals = freshDeskInsights.values("month").annotate(
            aes=Avg("aes"),
            resolved_count=Sum("resolved_count"),
            complaints=Sum("complaints"),
            csat=Avg("csat"),
            overall_score=Avg("overall_score"),
        )

        def calculate_grade(avg_score):
            if avg_score >= 5:
                return "A"
            elif avg_score >= 4:
                return "B"
            elif avg_score >= 3:
                return "C"
            else:
                return "D"

        totals = {
            item["month"]: {
                "aes": item["aes"],
                "resolved_count": item["resolved_count"],
                "complaints": item["complaints"],
                "csat": item["csat"],
                "overall_score": item["overall_score"],
                "grade": calculate_grade(item["overall_score"]),
            }
            for item in monthly_totals
        }

        calendar_ordered_totals = {
            month: totals[month] for month in calendar_order if month in totals
        }

        return Response(calendar_ordered_totals, status=status.HTTP_200_OK)


class GetUserFreshDeskInsightsStatisticsByRangeView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, user_id, year, start_month, end_month, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        freshDesk_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
            month__gte=start_month,
            month__lte=end_month,
        )

        if not freshDesk_insights.exists():
            return Response(
                {"message": "No freshDesk insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = freshDesk_insights.first().managed_by
        grade_counts = freshDesk_insights.values("grade").annotate(count=Count("grade"))

        all_freshDesk_insights_stats = {
            "Year": year,
            "start_month": start_month,
            "end_month": end_month,
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
                "aes": round(
                    freshDesk_insights.values("aes").aggregate(Avg("aes"))["aes__avg"],
                    2,
                ),
                "resolved_count": round(
                    freshDesk_insights.values("resolved_count").aggregate(
                        Avg("resolved_count")
                    )["resolved_count__avg"],
                    2,
                ),
                "average_complaints": round(
                    freshDesk_insights.values("complaints").aggregate(
                        Avg("complaints")
                    )["complaints__avg"],
                    2,
                ),
                "csat": round(
                    freshDesk_insights.values("csat").aggregate(Avg("csat"))[
                        "csat__avg"
                    ],
                    2,
                ),
                "overall_score": round(
                    freshDesk_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
        }

        return Response(all_freshDesk_insights_stats, status=status.HTTP_200_OK)


class GetUserFreshDeskTotalStatisticsByRangeView(GenericAPIView):
    permission_classes = []
    serializer_class = FreshDeskInsightsRetrieveSerializer
    queryset = FreshDeskInsights.objects.all()

    def get(self, request, user_id, year, start_month, end_month, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        freshDesk_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
            month__gte=start_month,
            month__lte=end_month,
        )

        if not freshDesk_insights.exists():
            return Response(
                {"message": "No freshDesk insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = freshDesk_insights.first().managed_by
        grade_counts = freshDesk_insights.values("grade").annotate(count=Count("grade"))

        all_freshDesk_insights_stats = {
            "Year": year,
            "start_month": start_month,
            "end_month": end_month,
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
            "total_stats": {
                "aes": sum(freshDesk_insights.values_list("aes", flat=True)),
                "resolved_count": sum(
                    freshDesk_insights.values_list("resolved_count", flat=True)
                ),
                "complaints": sum(
                    freshDesk_insights.values_list("complaints", flat=True)
                ),
                "csat": sum(freshDesk_insights.values_list("csat", flat=True)),
                "total_overall_score": sum(
                    freshDesk_insights.values_list("overall_score", flat=True)
                ),
            },
        }

        return Response(all_freshDesk_insights_stats, status=status.HTTP_200_OK)
