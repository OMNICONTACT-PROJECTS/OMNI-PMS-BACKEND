from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateAgentView.as_view(), name="create_agent"),
    path("<int:pk>/", views.AgentReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllAgents.as_view()),
]
