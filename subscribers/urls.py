from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateSubscriberView.as_view(), name="create_subscriber"),
    path("<int:pk>/", views.SubscriberReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllSubscribers.as_view()),
    path(
        "bulk-upload/",
        views.BulkUploadSubscriberDataView.as_view(),
        name="bulk-upload_subscriber",
    ),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllSubscriberByOrganisationId.as_view(),
    ),
    
]
