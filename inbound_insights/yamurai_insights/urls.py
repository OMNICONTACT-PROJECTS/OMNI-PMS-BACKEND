from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateYamuraiInsightsView.as_view(), name="create_yamurai_insights"),
    path(
        "bulk-upload/",
        views.BulkUploadYamuraiInsightsDataView.as_view(),
        name="bulk-upload_yamurai_insights",
    ),
    path(
        "upload-yamurai-insights-bulk-upload-template/",
        views.UploadYamuraiInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_yamurai_insights_template",
    ),
    path(
        "get-yamurai-insights-bulk-upload-template/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetYamuraiInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_yamurai_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetYamuraiInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.YamuraiInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.YamuraiInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllYamuraiInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetYamuraiInsightsByUserId.as_view()),
    path(
        "get-agents-by-organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsByDateAndOrganisationId.as_view(),
    ),
    path(
        "get-all-average-statists-by-organisation-id/<int:organisation_id>/agent-type/<str:agent_type>/",
        views.GetAllAverageYamuraiInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/week/<int:week>/agent_type/<str:agent_type>/",
        views.GetAllYamuraiInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.GetAllYamuraiInsightsStatisticsWithoutWeekView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.GetAllYamuraiInsightsStatisticsWithoutMonthAndWeekView.as_view(),
    ),
    ##########################
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.NewGetAllYamuraiInsightsStatisticsWithWeekView.as_view(),
    ),
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.NewGetAllYamuraiInsightsStatisticsWithMonthView.as_view(),
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
    path(
        "get-user-average-stats-by-range/<int:user_id>/year/<int:year>/start-month/<str:start_month>/end-month/<str:end_month>/",
        views.GetUserYamuraiInsightsStatisticsByRangeView.as_view(),
    ),
    path(
        "get-user-total-stats-by-range/<int:user_id>/year/<int:year>/start-month/<str:start_month>/end-month/<str:end_month>/",
        views.GetUserYamuraiInsightsTotalStatisticsByRangeView.as_view(),
    ),
]
