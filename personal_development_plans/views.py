from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)

from accounts.models import User
from personal_development_plans.models import Pdp, PdpReviewer
from personal_development_plans.serializers import PdpRetrieveSerializer, PdpReviewerRetrieveSerializer, PdpReviewerSerializer, PdpReviewerUpdateSerializer, PdpSerializer, PdpUpdateSerializer
from rest_framework import status

# Create your views here.

class CreatePdpView(CreateAPIView):
    permission_classes = []
    serializer_class = PdpSerializer
    queryset = Pdp.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Pdp created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Personal Development Plan, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Personal Development Plan. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllPdp(ListAPIView):
    permission_classes = []
    serializer_class = PdpRetrieveSerializer
    queryset = Pdp.objects.all()


class PdpReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = PdpRetrieveSerializer
    queryset = Pdp.objects.all()


class PdpUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = PdpUpdateSerializer
    queryset = Pdp.objects.all()


class GetPdpByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = PdpRetrieveSerializer
    queryset = Pdp.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            personal_development_plan = self.queryset.filter(user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(personal_development_plan, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        

# PdpReviewer

class CreatePdpReviewerView(CreateAPIView):
    permission_classes = []
    serializer_class = PdpReviewerSerializer
    queryset = PdpReviewer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Pdp Review created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Personal Development Plan Review, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Personal Development Plan Review. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllPdpReviewer(ListAPIView):
    permission_classes = []
    serializer_class = PdpReviewerRetrieveSerializer
    queryset = PdpReviewer.objects.all()


class PdpReviewerReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = PdpReviewerRetrieveSerializer
    queryset = PdpReviewer.objects.all()


class PdpReviewerUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = PdpReviewerUpdateSerializer
    queryset = PdpReviewer.objects.all()


class GetPdpReviewerByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = PdpReviewerRetrieveSerializer
    queryset = PdpReviewer.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            personal_development_plan_review = self.queryset.filter(user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(personal_development_plan_review, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)