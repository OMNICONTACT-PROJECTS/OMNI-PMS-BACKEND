from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreateYamuraiInsightsView.as_view(), name="create_yamurai_insights"
    ),
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
        "for-lvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsForLVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "for-hvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsForHVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetYamuraiInsightsByDateAndOrganisationId.as_view(),
    ),
]
