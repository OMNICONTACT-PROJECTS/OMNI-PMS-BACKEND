from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateScorecardView.as_view(), name="Scorecard"),
    path("bulky-create", views.CreateBulkyScorecardView.as_view(), name="bulky_scorecards"),

    path("<int:pk>/", views.ScorecardReadDestroyView.as_view()),
    path("update/<int:pk>/", views.ScorecardUpdateView.as_view()),
    path("get-all/", views.GetAllScorecard.as_view()),
    path("get-by-user-id/<int:user_id>/", views.GetScorecardByUserId.as_view()),
    path(
        "get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllScorecardByOrganisationId.as_view(),
    ),
    path("strategy/", views.CreateStrategyView.as_view(), name="Strategy"),
    path("strategy/<int:pk>/", views.StrategyReadDestroyView.as_view()),
    path("strategy/update/<int:pk>/", views.StrategyUpdateView.as_view()),
    path("strategy/get-all/", views.GetAllStrategies.as_view()),
    path("strategy/get-by-user-id/<int:user_id>/", views.GetStrategyByUserId.as_view()),
    path(
        "strategy/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllStrategiesByOrganisationId.as_view(),
    ),
    path("function/", views.CreateFunctionView.as_view(), name="Function"),
    path("function/<int:pk>/", views.FunctionReadDestroyView.as_view()),
    path("function/update/<int:pk>/", views.FunctionUpdateView.as_view()),
    path("function/get-all/", views.GetAllFunctions.as_view()),
    path("function/get-by-user-id/<int:user_id>/", views.GetFunctionByUserId.as_view()),
    path(
        "function/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllFunctionsByOrganisationId.as_view(),
    ),
    path("customer/", views.CreateCustomerView.as_view(), name="Customer"),
    path("customer/<int:pk>/", views.CustomerReadDestroyView.as_view()),
    path("customer/update/<int:pk>/", views.CustomerUpdateView.as_view()),
    path("customer/get-all/", views.GetAllCustomers.as_view()),
    path("customer/get-by-user-id/<int:user_id>/", views.GetCustomerByUserId.as_view()),
    path(
        "customer/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllCustomersByOrganisationId.as_view(),
    ),
    path("innovation/", views.CreateInnovationView.as_view(), name="Innovation"),
    path("innovation/<int:pk>/", views.InnovationReadDestroyView.as_view()),
    path("innovation/update/<int:pk>/", views.InnovationUpdateView.as_view()),
    path("innovation/get-all/", views.GetAllInnovations.as_view()),
    path(
        "innovation/get-by-user-id/<int:user_id>/",
        views.GetInnovationByUserId.as_view(),
    ),
    path(
        "innovation/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllInnovationsByOrganisationId.as_view(),
    ),
    path("operation/", views.CreateOperationView.as_view(), name="Operation"),
    path("operation/<int:pk>/", views.OperationReadDestroyView.as_view()),
    path("operation/update/<int:pk>/", views.OperationUpdateView.as_view()),
    path("operation/get-all/", views.GetAllOperations.as_view()),
    path(
        "operation/get-by-user-id/<int:user_id>/", views.GetOperationByUserId.as_view()
    ),
    path(
        "operation/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllOperationsByOrganisationId.as_view(),
    ),
    path(
        "review",
        views.CreateScorecardReviewView.as_view(),
        name="Scorecard_reviewer",
    ),
    path("review/<int:pk>/", views.ScorecardReviewReadDestroyView.as_view()),
    path("review/update/<int:pk>/", views.ScorecardReviewUpdateView.as_view()),
    path("review/get-all/", views.GetAllScorecardReview.as_view()),
    path(
        "review/get-by-user-id/<int:user_id>/",
        views.GetScorecardReviewByUserId.as_view(),
    ),
    path(
        "review/get-all-by-organisation-id/<int:organisation_id>/",
        views.GetAllScorecardReviewByOrganisationId.as_view(),
    ),
    path("status/update/<int:pk>/", views.ScorecardStatusUpdateView.as_view()),
]
