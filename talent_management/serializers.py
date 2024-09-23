from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.models import Group, Permission

    
class UserUploadProfPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['User', 'file']