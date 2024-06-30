from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateVoiceInsightsView.as_view(), name="create_voice_insights"),
    path(
        "bulk-upload/",
        views.BulkUploadVoiceInsightsDataView.as_view(),
        name="bulk-upload_voice_insights",
    ),
    path(
        "upload-voice-insights-bulk-upload-template/",
        views.UploadVoiceInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_voice_insights_template",
    ),
    path(
        "get-voice-insights-bulk-upload-template/<int:organisation_id>/",
        views.GetVoiceInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_voice_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/",
        views.GetVoiceInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.VoiceInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.VoiceInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllVoiceInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetVoiceInsightsByUserId.as_view()),
    path(
        "for-lvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetVoiceInsightsForLVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "for-hvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetVoiceInsightsForHVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetVoiceInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetVoiceInsightsByDateAndOrganisationId.as_view(),
    ),
]
