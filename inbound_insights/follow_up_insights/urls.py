from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreateFollowUpInsightsView.as_view(), name="create_followup_insights"
    ),
    path(
        "bulk-upload/",
        views.BulkUploadFollowUpInsightsDataView.as_view(),
        name="bulk-upload_follow_up_insights",
    ),
    path(
        "upload-follow-up-insights-bulk-upload-template/",
        views.UploadFollowUpInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_follow_up_insights_template",
    ),
    path(
        "get-follow-up-insights-bulk-upload-template/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetFollowUpInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_follow_up_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetFollowUpInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.FollowUpInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.FollowUpInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllFollowUpInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetFollowUpInsightsByUserId.as_view()),
    path(
        "for-lvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetFollowUpInsightsForLVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "for-hvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetFollowUpInsightsForHVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetFollowUpInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetFollowUpInsightsByDateAndOrganisationId.as_view(),
    ),
]
