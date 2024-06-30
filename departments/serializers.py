from rest_framework.serializers import ModelSerializer
from .models import Department



class DepartmentSerializer(ModelSerializer):
    class meta:
        model = Department
        fields = ('__all__')

        


