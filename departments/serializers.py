from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group, Permission

from departments.models import Department



class DepartmentSerializer(ModelSerializer):
    class Meta:
        model= Department
        fields= "__all__"
        extra_kwargs = {
            "organisation": {"required": True},
            "name": {"required": True},
        }
  



        

