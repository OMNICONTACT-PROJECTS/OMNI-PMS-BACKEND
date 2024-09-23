from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserWorkExperienceCreate.as_view()),
    path("get-all/", views.UserWorkExperienceGetAll.as_view()),
    path("<int:pk>/", views.UserWorkExperienceGetUpdateDeleteByID.as_view()),
]
