from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateAdministratorView.as_view(), name="create_administrator"),
    path("<int:pk>/", views.AdministratorReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllAdministrators.as_view()),
]
