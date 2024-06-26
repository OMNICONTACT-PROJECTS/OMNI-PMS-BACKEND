from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateOrganisationView.as_view(), name="create_organisation"),
    path("<int:pk>/", views.OrganisationReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllOrganisations.as_view()),
]
