from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreatePdpView.as_view(), name="create_personal_development_plan/"
    ),
    path("<int:pk>/", views.PdpReadDestroyView.as_view()),
    path("update/<int:pk>/", views.PdpUpdateView.as_view()),
    path("get-all/", views.GetAllPdp.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetPdpByUserId.as_view()),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllPdpByOrganisationId.as_view(),
    ),

    path(
        "pdp-reviewer", views.CreatePdpReviewerView.as_view(), name="create_personal_development_plan_reviewer"
    ),
    path("pdp-reviewer/<int:pk>/", views.PdpReviewerReadDestroyView.as_view()),
    path("pdp-reviewer/update/<int:pk>/", views.PdpReviewerUpdateView.as_view()),
    path("pdp-reviewer/get-all/", views.GetAllPdpReviewer.as_view()),
    path("pdp-reviewer/get-by-user-id/<int:user_id>/", views.GetPdpReviewerByUserId.as_view()),
    path(
        "pdp-reviewer/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllPdpReviewerByOrganisationId.as_view(),
    ),
    
]
