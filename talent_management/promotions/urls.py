from django.urls import path
from . import views

urlpatterns = [
    path("", views.PromotionCreateView.as_view()),
    path("get-all/", views.PromotionGetAll.as_view()),
    path("<int:pk>/", views.PromotionGetDeleteByID.as_view()),
    path("update/<int:pk>/", views.UpdatePromotion.as_view()),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllPromotionsByOrganisationId.as_view(),
    ),
    path("get-by-user-id/<int:user_id>/", views.GetPromotionsByUserId.as_view()),
    path("update-status/<int:pk>/", views.UpdatePromotionStatus.as_view()),
]
