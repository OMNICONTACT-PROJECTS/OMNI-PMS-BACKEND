from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreateFreshChatInsightsView.as_view(), name="create_fresh_chat_insights"
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
]
