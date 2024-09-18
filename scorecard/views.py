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
from .models import Scorecard, ScorecardClone, ScorecardReview, Customer, Function, Strategy, Innovation, Operations
from .serializers import (
    ScorecardRetrieveSerializer,
    ScorecardSerializer,
)
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

class CreateScorecardView(CreateAPIView):
    permission_classes = []
    serializer_class = ScorecardSerializer
    queryset = Scorecard.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Scorecard created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Scorecard, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Scorecard. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllScorecard(ListAPIView):
    permission_classes = []
    serializer_class = ScorecardRetrieveSerializer
    queryset = Scorecard.objects.all()


class ScorecardReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = ScorecardRetrieveSerializer
    queryset = Scorecard.objects.all()


# class ScorecardUpdateView(UpdateAPIView):
#     permission_classes = []
#     serializer_class = ScorecardUpdateSerializer
#     queryset = Scorecard.objects.all()


# class GetScorecardByUserId(GenericAPIView):
#     permission_classes = []
#     serializer_class = ScorecardRetrieveSerializer
#     queryset = Scorecard.objects.all()

#     def get(self, request, user_id, *args, **kwargs):
#         try:
#             User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
#         else:
#             personal_development_plan = self.queryset.filter(user_id=user_id).order_by(
#                 "-date_created"
#             )
#             serializer = self.serializer_class(personal_development_plan, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)


# class GetAllScorecardByOrganisationId(GenericAPIView):
#     permission_classes = []
#     serializer_class = ScorecardRetrieveSerializer
#     queryset = Scorecard.objects.all()

#     def get(self, request, organisation_id):
#         try:
#             organisation = Organisation.objects.get(pk=organisation_id)
#         except Organisation.DoesNotExist:
#             return Response(
#                 data={"message": "Organisation does not exist"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         else:
#             Scorecard_info_by_organisation = self.queryset.filter(
#                 user__organisation_id=organisation_id
#             )
#             serializer = self.serializer_class(Scorecard_info_by_organisation, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)


# # ScorecardReviewer

# class CreateScorecardReviewerView(CreateAPIView):
#     permission_classes = []
#     serializer_class = ScorecardReviewerSerializer
#     queryset = ScorecardReviewer.objects.all()

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             try:
#                 Scorecard = Scorecard.objects.get(pk=request.data.get("Scorecard"))
#             except Scorecard.DoesNotExist:
#                 return Response(
#                     {"message": "Selected Scorecard does not exist"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             user_data = User.objects.get(pk=request.data.get("user"))
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "User does not exist"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         try:

#             if serializer.is_valid():
#                 self.perform_create(serializer)
#                 data = {
#                     "message": "Scorecard Review created successfully",
#                     "data": serializer.data,
#                 }
#                 print(
#                     "user", user_data.first_name, user_data.last_name, user_data.email
#                 )

#                 first_name = user_data.first_name.upper()

#                 last_name = user_data.last_name.upper()
#                 email = user_data.email
#                 full_name = f"{first_name } { last_name}"

#                 email_subject = f"Your Scorecard Has Been Reviewed"
#                 email_to = email
#                 email_from = settings.EMAIL_HOST_USER
#                 email_body = (
#                     f"Dear {full_name},\n\nWe are pleased to inform you that your Scorecard (Scorecard) has been reviewed by our HR Administration Team. You can now log in to your account to view the feedback and any necessary next steps."
#                     f"Thank you for your commitment to your personal development!. You can login on the PMS Platform to access your reviewed Scorecard\n\n"
#                     f"Feel free to reach out to our support team at support@omnicontact.biz for assistance with anything.\n\n"
#                     f"Best regards,\n"
#                     f"OMNICONTACT DEV\n"
#                 )

#                 send_mail(
#                     email_subject,
#                     email_body,
#                     email_from,
#                     [email_to],
#                     fail_silently=True,
#                 )
#                 return Response(data, status=status.HTTP_201_CREATED)

#             return Response(
#                 {
#                     "message": "Failed to create Scorecard Review, Validation error occurred.",
#                     "error": serializer.errors,
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         except Exception as e:
#             return Response(
#                 {
#                     "message": "Failed to create Scorecard Review. Exception error occurred",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# class GetAllScorecardReviewer(ListAPIView):
#     permission_classes = []
#     serializer_class = ScorecardReviewerRetrieveSerializer
#     queryset = ScorecardReviewer.objects.all()


# class ScorecardReviewerReadDestroyView(RetrieveDestroyAPIView):
#     permission_classes = []
#     serializer_class = ScorecardReviewerRetrieveSerializer
#     queryset = ScorecardReviewer.objects.all()


# class ScorecardReviewerUpdateView(UpdateAPIView):
#     permission_classes = []
#     serializer_class = ScorecardReviewerUpdateSerializer
#     queryset = ScorecardReviewer.objects.all()


# class GetScorecardReviewerByUserId(GenericAPIView):
#     permission_classes = []
#     serializer_class = ScorecardReviewerRetrieveSerializer
#     queryset = ScorecardReviewer.objects.all()

#     def get(self, request, user_id, *args, **kwargs):
#         try:
#             User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return Response(
#                 {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
#         else:
#             personal_development_plan_review = self.queryset.filter(
#                 user_id=user_id
#             ).order_by("-date_created")
#             serializer = self.serializer_class(
#                 personal_development_plan_review, many=True
#             )
#             return Response(data=serializer.data, status=status.HTTP_200_OK)


# class GetAllScorecardReviewerByOrganisationId(GenericAPIView):
#     permission_classes = []
#     serializer_class = ScorecardReviewerSerializer
#     queryset = ScorecardReviewer.objects.all()

#     def get(self, request, organisation_id):
#         try:
#             organisation = Organisation.objects.get(pk=organisation_id)
#         except Organisation.DoesNotExist:
#             return Response(
#                 data={"message": "Organisation does not exist"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         else:
#             Scorecard_reviewer_info_by_organisation = self.queryset.filter(
#                 user__organisation_id=organisation_id
#             )
#             serializer = self.serializer_class(
#                 Scorecard_reviewer_info_by_organisation, many=True
#             )
#             return Response(serializer.data, status=status.HTTP_200_OK)


# class ScorecardStatusUpdateView(GenericAPIView):
#     permission_classes = []
#     serializer_class = ScorecardUpdateStatusSerializer
#     queryset = Scorecard.objects.all()

#     def put(self, request, Scorecard_id):
#         try:
#             Scorecard = Scorecard.objects.get(pk=Scorecard_id)
#         except Scorecard.DoesNotExist:
#             return Response(
#                 {"message": "Scorecard does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
#         else:
#             Scorecard.status = "APPROVED"
#             Scorecard.save()
#             return Response(
#                 {
#                     "message": "Scorecard status updated successfully",
#                 },
#                 status=status.HTTP_200_OK,
#             )
