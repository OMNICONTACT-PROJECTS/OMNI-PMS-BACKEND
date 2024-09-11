from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateSasaiInsightsView.as_view(), name="create_sasai_insights"),
    path(
        "bulk-upload/",
        views.BulkUploadSasaiInsightsDataView.as_view(),
        name="bulk-upload_sasai_insights",
    ),
    path(
        "upload-sasai-insights-bulk-upload-template/",
        views.UploadSasaiInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_sasai_insights_template",
    ),
    path(
        "get-sasai-insights-bulk-upload-template/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetSasaiInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_sasai_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetSasaiInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.SasaiInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.SasaiInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllSasaiInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetSasaiInsightsByUserId.as_view()),
    path(
        "get-agents-by-organisation_id/<int:organisation_id>/",
        views.GetSasaiInsightsAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetSasaiInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetSasaiInsightsByDateAndOrganisationId.as_view(),
    ),
    path(
        "get-all-average-statists-by-organisation-id/<int:organisation_id>/agent-type/<str:agent_type>/",
        views.GetAllAverageSasaiInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/week/<int:week>/agent_type/<str:agent_type>/",
        views.GetAllSasaiInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.GetAllSasaiInsightsStatisticsWithoutWeekView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.GetAllSasaiInsightsStatisticsWithoutMonthAndWeekView.as_view(),
    ),
    ##########################
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.NewGetAllSasaiInsightsStatisticsWithWeekView.as_view(),
    ),
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.NewGetAllSasaiInsightsStatisticsWithMonthView.as_view(),
    ),
    path(
        "get-user-monthly-statistics-by-user-id/<int:user_id>/year/<int:year>/month/<str:month>/",
        views.GetUserMonthlyInsightsStatisticsView.as_view(),
    ),
    path(
        "get-user-yearly-statistics-by-user-id/<int:user_id>/year/<int:year>/",
        views.GetUserYearlyInsightsStatisticsView.as_view(),
    ),
    path(
        "get-total-monthly-statistics-by-organisation-id/<int:organisation_id>/user-id/<int:user_id>/year/<int:year>/agent-type/<str:agent_type>/",
        views.GetAllInsightsMonthlyStatisticsPerUserView.as_view(),
    ),
]
