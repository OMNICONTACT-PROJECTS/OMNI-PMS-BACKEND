from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenObtainPairView,
)
from . import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
    path("verify-password/", views.verify_pwd),
    path("change-password/", views.change_pwd),
]
