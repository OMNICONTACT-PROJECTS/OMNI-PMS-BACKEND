from ..models import Promotion
from accounts.models import User
from .serializers import PromotionSerializer, RetrievePromotionSerializer, PromotionStatusSerializer
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    UpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from organisations.models import Organisation


class PromotionCreateView(CreateAPIView):
    permission_classes = []
    serializer_class = PromotionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Promotions created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create promotion, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create promotion. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class PromotionGetAll(GenericAPIView):
    permission_classes = []
    serializer_class = RetrievePromotionSerializer
    queryset = Promotion.objects.all()

    def get(self, request):
        promotions = self.queryset.all()
        serializer = self.serializer_class(promotions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PromotionGetAll(GenericAPIView):
    permission_classes = []
    serializer_class = RetrievePromotionSerializer
    queryset = Promotion.objects.all()

    def get(self, request):
        promotions = self.queryset.all()
        serializer = self.serializer_class(promotions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PromotionGetDeleteByID(GenericAPIView):
    permission_classes = []
    serializer_class = RetrievePromotionSerializer
    queryset = Promotion.objects.all()

    def get(self, request, pk):
        try:
            promotions = self.queryset.get(pk=pk)
        except Promotion.DoesNotExist:
            return Response(
                data={"error": "promotions not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(promotions)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            promotions = self.queryset.get(pk=pk)
        except Promotion.DoesNotExist:
            return Response(
                data={"error": "Promotion not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            promotions.delete()
            return Response(
                data={"message": "Promotion deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )


class UpdatePromotion(GenericAPIView):
    permission_classes = []
    serializer_class = PromotionSerializer
    queryset = Promotion.objects.all()

    def put(self, request, pk):
        try:
            promotions = self.queryset.get(pk=pk)
        except Promotion.DoesNotExist:
            return Response(
                data={"error": "Promotion not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(
                promotions, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.data,
                    "message": "Promotion Updated successfully",
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPromotionsByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrievePromotionSerializer
    queryset = Promotion.objects.all()

    def get(self, request, user_id):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            work_promotions = self.queryset.filter(user_id=user_id)
            serializer = self.serializer_class(work_promotions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllPromotionsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = RetrievePromotionSerializer
    queryset = Promotion.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            work_promotions = self.queryset.filter(
                user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(work_promotions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UpdatePromotionStatus(GenericAPIView):
    permission_classes = []
    serializer_class = PromotionStatusSerializer
    queryset = Promotion.objects.all()

    def put(self, request, pk):
        try:
            promotion = self.queryset.get(pk=pk)
        except Promotion.DoesNotExist:
            return Response(
                data={"error": "Promotion not Found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = self.serializer_class(
                promotion, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                data = {
                    "data": serializer.data,
                    "message": "Status Updated successfully",
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
