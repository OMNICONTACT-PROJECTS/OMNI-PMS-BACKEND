from django.urls import path
from . import views

urlpatterns = [
    path("",views.CreateDepartmentView.as_view(),name="create_department"),
    path("<int:pk>/",views.RetrieveDepartmentView.as_view(),name="get_department"),
    path("update/<int:pk>/",views.UpdateDepartmentView.as_view(),name="get_department"),
    path("get-all/",views.ListDepartmentView.as_view(),name="all_departments"),
    path("get-all-by-organisation-id/<int:organisation_id>/",views.GetDepartmentByOrganisationView.as_view(),name="all_departments"),
]