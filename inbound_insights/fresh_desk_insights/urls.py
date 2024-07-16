from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreateFreshDeskInsightsView.as_view(), name="create_fresh_desk_insights"
    ),
    path(
        "bulk-upload/",
        views.BulkUploadFreshDeskInsightsDataView.as_view(),
        name="bulk-upload_fresh_desk_insights",
    ),
    path(
        "upload-fresh-desk-insights-bulk-upload-template/",
        views.UploadFreshDeskInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_fresh_desk_insights_template",
    ),
    path(
        "get-fresh-desk-insights-bulk-upload-template/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetFreshDeskInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_fresh_desk_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetFreshDeskInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.FreshDeskInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.FreshDeskInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllFreshDeskInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetFreshDeskInsightsByUserId.as_view()),
    path(
        "for-lvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetFreshDeskInsightsForLVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "for-hvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetFreshDeskInsightsForHVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetFreshDeskInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetFreshDeskInsightsByDateAndOrganisationId.as_view(),
    ),
    path(
        "get-all-average-statists-by-organisation-id/<int:organisation_id>/agent-type/<str:agent_type>/",
        views.GetAllAverageFreshDeskInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/week/<int:week>/agent_type/<str:agent_type>/",
        views.GetAllFreshDeskInsightsStatisticsView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.GetAllFreshDeskInsightsStatisticsWithoutWeekView.as_view(),
    ),
    path(
        "get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.GetAllFreshDeskInsightsStatisticsWithoutMonthAndWeekView.as_view(),
    ),

    ##########################

    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/month/<str:month>/agent_type/<str:agent_type>/",
        views.NewGetAllFreshDeskInsightsStatisticsWithWeekView.as_view(),
    ),
    path(
        "new-get-all-statistics-by-organisation-id/<int:organisation_id>/year/<int:year>/agent_type/<str:agent_type>/",
        views.NewGetAllFreshDeskInsightsStatisticsWithMonthView.as_view(),
    ),
]
