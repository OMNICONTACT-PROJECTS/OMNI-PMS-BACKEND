from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import User
from .serializers import UserSerializer


class UserView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = UserSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_pwd(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.data["username"])
            pwd_valid = check_password(request.data["password"], user.password)
            if pwd_valid:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_pwd(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.data["username"])
            user.set_password(request.data["password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_403_FORBIDDEN)
