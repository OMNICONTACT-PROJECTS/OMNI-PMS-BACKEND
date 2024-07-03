from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveDestroyAPIView,

)
from rest_framework import  status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

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
