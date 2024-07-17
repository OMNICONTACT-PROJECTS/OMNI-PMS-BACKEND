from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveDestroyAPIView,
    GenericAPIView
)
from rest_framework import  status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from organisations.models import Organisation
from departments.models import Department
from departments.serializers import  DepartmentSerializer, DepartmentRetrieveSerializer

# Create your views here.

class CreateDepartmentView(CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []

class ListDepartmentView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentRetrieveSerializer
    permission_classes = []



class RetrieveDepartmentView(RetrieveDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentRetrieveSerializer
    permission_classes = []


class UpdateDepartmentView(UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []

class GetDepartmentByOrganisationView(GenericAPIView):
    permission_classes = []
    serializer_class = DepartmentRetrieveSerializer
    queryset = Department.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            departments = self.queryset.filter(organisation_id=organisation_id)
            serializer = self.serializer_class(departments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

