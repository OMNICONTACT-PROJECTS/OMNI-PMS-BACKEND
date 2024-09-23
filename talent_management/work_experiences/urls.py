from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserWorkExperienceCreate.as_view()),
    path("get-all/", views.UserWorkExperienceGetAll.as_view()),
    path("<int:pk>/", views.UserWorkExperienceGetUpdateDeleteByID.as_view()),
    path(
        "update/<int:pk>/", views.UpdateUserWorkExperienceGetUpdateDeleteByID.as_view()
    ),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllWorkExperienceByOrganisationId.as_view(),
    ),
    path(
        "get-by-user-id/<int:user_id>/", views.GetWorkExperienceByUserId.as_view()
    ),
]
