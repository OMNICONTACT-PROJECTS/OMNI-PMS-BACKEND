from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreateHigherLifeFoundationInsightsView.as_view(), name="create_higherLifeFoundation_insights"
    ),
    path(
        "bulk-upload/",
        views.BulkUploadHigherLifeFoundationInsightsDataView.as_view(),
        name="bulk-upload_higher_life_foundation_insights",
    ),
    path(
        "upload-higher-life-foundation-insights-bulk-upload-template/",
        views.UploadHigherLifeFoundationInsightsBulkUploadTemplate.as_view(),
        name="bulk-upload_higher_life_foundation_insights_template",
    ),
    path(
        "get-higher-life-foundation-insights-bulk-upload-template/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetHigherLifeFoundationInsightsBulkUploadTemplate.as_view(),
        name="get_bulk-upload_higher_life_foundation_insights_template",
    ),
    path(
        "get-all-bulk-upload-files-by-organisation-id/<int:organisation_id>/campaign/<str:campaign_name>/",
        views.GetHigherLifeFoundationInsightsUploadedFilesView.as_view(),
    ),
    path("<int:pk>/", views.HigherLifeFoundationInsightsReadDestroyView.as_view()),
    path("update/<int:pk>/", views.HigherLifeFoundationInsightsUpdateView.as_view()),
    path("get-all/", views.GetAllHigherLifeFoundationInsights.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetHigherLifeFoundationInsightsByUserId.as_view()),
    path(
        "for-lvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetHigherLifeFoundationInsightsForLVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "for-hvc-agents-by-organisation_id/<int:organisation_id>/",
        views.GetHigherLifeFoundationInsightsForHVCAgentsByOrganisationId.as_view(),
    ),
    path(
        "get-by-grade/<str:grade>/organisation_id/<int:organisation_id>/",
        views.GetHigherLifeFoundationInsightsByGradeAndOrganisationId.as_view(),
    ),
    path(
        "get-by-date/year/<int:year>/month/<str:month>/week/<int:week>/organisation_id/<int:organisation_id>/",
        views.GetHigherLifeFoundationInsightsByDateAndOrganisationId.as_view(),
    ),
]
