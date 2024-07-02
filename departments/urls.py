from django.urls import path
from . import views

urlpatterns = [
    path("",views.CreateDepartmentView.as_view(),name="create_department"),
    path("<int:pk>/",views.RetrieveDepartmentView.as_view(),name="get_department"),
    path("get-all/",views.ListDepartmentView.as_view(),name="all_departments"),
]