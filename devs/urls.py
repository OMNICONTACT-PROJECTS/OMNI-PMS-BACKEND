from django.urls import path
from devs import views

urlpatterns = [
    path("", views.CreateDevView.as_view(), name="create_dev"),
    path("<int:pk>/", views.DevReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllDevs.as_view()),
]
