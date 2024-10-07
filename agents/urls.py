from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateAgentView.as_view(), name="create_agent"),
    path(
        "bulk-upload/",
        views.BulkUploadAgentDataView.as_view(),
        name="bulk-upload_agents",
    ),
    path("<int:pk>/", views.AgentReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllAgents.as_view()),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllAgentByOrganisationId.as_view(),
    ),
    path(
        "get-all-by-user-id/<int:user_id>/",
        views.GetAllAgentByUserId.as_view(),
    ),
]
