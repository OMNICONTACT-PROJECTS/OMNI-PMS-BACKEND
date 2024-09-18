from django.urls import path
from . import views

urlpatterns = [
    path(
        "", views.CreateScorecardView.as_view(), name="Scorecard/"
    ),
    path("<int:pk>/", views.ScorecardReadDestroyView.as_view()),
    # path("update/<int:pk>/", views.ScorecardUpdateView.as_view()),
    path("get-all/", views.GetAllScorecard.as_view()),
    # path("get-by-user-id/<int:user_id>/", views.GetScorecardByUserId.as_view()),
    # path(
    #     "get-all-by-organisation-id/<int:organisation_id>/",
    #     views.GetAllScorecardByOrganisationId.as_view(),
    # ),

    # path(
    #     "Scorecard-reviewer", views.CreateScorecardReviewerView.as_view(), name="Scorecard_reviewer"
    # ),
    # path("Scorecard-reviewer/<int:pk>/", views.ScorecardReviewerReadDestroyView.as_view()),
    # path("Scorecard-reviewer/update/<int:pk>/", views.ScorecardReviewerUpdateView.as_view()),
    # path("Scorecard-reviewer/get-all/", views.GetAllScorecardReviewer.as_view()),
    # path("Scorecard-reviewer/get-by-user-id/<int:user_id>/", views.GetScorecardReviewerByUserId.as_view()),
    # path(
    #     "Scorecard-reviewer/get-all-by-organisation-id/<int:organisation_id>/",
    #     views.GetAllScorecardReviewerByOrganisationId.as_view(),
    # ),
    # path("status/update/<int:Scorecard_id>/", views.ScorecardStatusUpdateView.as_view()),
]
