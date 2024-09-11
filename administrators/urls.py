from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateAdministratorView.as_view(), name="create_administrator"),
    path("<int:pk>/", views.AdministratorReadDestroyView.as_view()),
    path("update/<int:pk>/", views.AdministratorUpdateView.as_view()),
    path("get-all/", views.GetAllAdministrators.as_view()),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllAdministratorByOrganisationId.as_view(),
    ),
]
