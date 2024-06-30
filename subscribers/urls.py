from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateSubscriberView.as_view(), name="create_subscriber"),
    path("<int:pk>/", views.SubscriberReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllSubscribers.as_view()),
]
