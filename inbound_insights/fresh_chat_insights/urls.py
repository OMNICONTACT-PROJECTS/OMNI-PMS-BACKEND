from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.CreateFreshChatInsightsView.as_view(),
        name="create_fresh_chat_insights",
    ),
    path(
        "bulk-upload/",
        views.BulkUploadFreshChatInsightsDataView.as_view(),
        name="bulk-upload_fresh_chat_insights",
    ),
    path(
        "upload-fresh-chat-insights-bulk-upload-template/",
        views.UploadFreshChatInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_fresh_chat_insights_template",
    ),
    path(
        "get-fresh-chat-insights-bulk-upload-template/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetFreshChatInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_fresh_chat_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetFreshChatInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.FreshChatInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.FreshChatInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllFreshChatInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetFreshChatInsightsByUserId.as_view()),
    path(
        "for-lvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetFreshChatInsightsForLVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "for-hvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetFreshChatInsightsForHVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetFreshChatInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetFreshChatInsightsByDateAndOrganisationId.as_view(),
    ),
    path(
        "get-all-average-statists-by-organisation-id/<int:organisation_id>/agent-type/<str:agent_type>/",
        views.GetAllAverageFreshChatInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/week/<int:week>/agent_type/<str:agent_type>/",
        views.GetAllFreshChatInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.GetAllFreshChatInsightsStatisticsWithoutWeekView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.GetAllFreshChatInsightsStatisticsWithoutMonthAndWeekView.as_view(),
    ),
    ##########################
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.NewGetAllFreshChatInsightsStatisticsWithWeekView.as_view(),
    ),
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.NewGetAllFreshChatInsightsStatisticsWithMonthView.as_view(),
    ),
    path(
        "get-user-monthly-statistics-by-user-id/<int:user_id>/year/<int:year>/month/<str:month>/",
        views.GetUserMonthlyInsightsStatisticsView.as_view(),
    ),
    path(
        "get-user-yearly-statistics-by-user-id/<int:user_id>/year/<int:year>/",
        views.GetUserYearlyInsightsStatisticsView.as_view(),
    ),
]
