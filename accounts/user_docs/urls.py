from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserPersonalDocumentCreate.as_view()),
    path("<int:pk>/", views.UserPersonalDocumentUpdateGetDeleteByID.as_view()),
    path("get-all/", views.GetAllUserDocsView.as_view()),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllDocumentsByOrganisationId.as_view(),
    ),
    path("update/<int:pk>/", views.UpdateUserDocsView.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetDocumentsByUserId.as_view()),
]
