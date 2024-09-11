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
from organisations.models import Organisation
from personal_development_plans.models import Pdp, PdpReviewer
from personal_development_plans.serializers import (
    PdpRetrieveSerializer,
    PdpReviewerRetrieveSerializer,
    PdpReviewerSerializer,
    PdpReviewerUpdateSerializer,
    PdpSerializer,
    PdpUpdateSerializer,
    PdpUpdateStatusSerializer,
)
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

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


class GetAllPdpByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = PdpRetrieveSerializer
    queryset = Pdp.objects.all()

    def get(self, request, organisation_id):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            pdp_info_by_organisation = self.queryset.filter(
                user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(pdp_info_by_organisation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# PdpReviewer

class CreatePdpReviewerView(CreateAPIView):
    permission_classes = []
    serializer_class = PdpReviewerSerializer
    queryset = PdpReviewer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            try:
                pdp = Pdp.objects.get(pk=request.data.get("pdp"))
            except Pdp.DoesNotExist:
                return Response(
                    {"message": "Selected PDP does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            user_data = User.objects.get(pk=request.data.get("user"))
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Pdp Review created successfully",
                    "data": serializer.data,
                }
                print(
                    "user", user_data.first_name, user_data.last_name, user_data.email
                )

                first_name = user_data.first_name.upper()

                last_name = user_data.last_name.upper()
                email = user_data.email
                full_name = f"{first_name } { last_name}"

                email_subject = f"Your PDP Has Been Reviewed"
                email_to = email
                email_from = settings.EMAIL_HOST_USER
                email_body = (
                    f"Dear {full_name},\n\nWe are pleased to inform you that your Personal Development Plan (PDP) has been reviewed by our HR Administration Team. You can now log in to your account to view the feedback and any necessary next steps."
                    f"Thank you for your commitment to your personal development!. You can login on the PMS Platform to access your reviewed PDP\n\n"
                    f"Feel free to reach out to our support team at support@omnicontact.biz for assistance with anything.\n\n"
                    f"Best regards,\n"
                    f"OMNICONTACT DEV\n"
                )

                send_mail(
                    email_subject,
                    email_body,
                    email_from,
                    [email_to],
                    fail_silently=True,
                )
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
            personal_development_plan_review = self.queryset.filter(
                user_id=user_id
            ).order_by("-date_created")
            serializer = self.serializer_class(
                personal_development_plan_review, many=True
            )
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllPdpReviewerByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = PdpReviewerSerializer
    queryset = PdpReviewer.objects.all()

    def get(self, request, organisation_id):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            pdp_reviewer_info_by_organisation = self.queryset.filter(
                user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(
                pdp_reviewer_info_by_organisation, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class PdpStatusUpdateView(GenericAPIView):
    permission_classes = []
    serializer_class = PdpUpdateStatusSerializer
    queryset = Pdp.objects.all()

    def put(self, request, pdp_id):
        try:
            pdp = Pdp.objects.get(pk=pdp_id)
        except Pdp.DoesNotExist:
            return Response(
                {"message": "PDP does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            pdp.status = "APPROVED"
            pdp.save()
            return Response(
                {
                    "message": "Pdp status updated successfully",
                },
                status=status.HTTP_200_OK,
            )
