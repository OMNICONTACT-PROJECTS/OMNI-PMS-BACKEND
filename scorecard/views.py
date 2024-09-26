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
from .models import (
    Scorecard,
    ScorecardClone,
    ScorecardReview,
    Strategy,
    Customer,
    Function,
    Innovation,
    Operation,
)
from .serializers import (
    ScorecardRetrieveSerializer,
    ScorecardSerializer,
    ScorecardUpdateSerializer,
    StrategySerializer,
    CustomerSerializer,
    FunctionSerializer,
    InnovationSerializer,
    OperationSerializer,
    ScorecardReviewSerializer,
    ScorecardReviewRetrieveSerializer,
    ScorecardReviewUpdateSerializer,
    ScorecardUpdateStatusSerializer,
    ScorecardBulkyCreateSerializer
)
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.parsers import FormParser, MultiPartParser

# Create your views here.


class CreateBulkyScorecardView(CreateAPIView):
    permission_classes = []
    serializer_class = ScorecardBulkyCreateSerializer
    queryset = Scorecard.objects.all()

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


class ScorecardUpdateView(UpdateAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser]
    serializer_class = ScorecardUpdateSerializer
    queryset = Scorecard.objects.all()


class GetScorecardByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = ScorecardRetrieveSerializer
    queryset = Scorecard.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            scorecard = self.queryset.filter(user_id=user_id).order_by("-date_created")
            serializer = self.serializer_class(scorecard, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllScorecardByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = ScorecardRetrieveSerializer
    queryset = Scorecard.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            scorecard_info_by_organisation = self.queryset.filter(
                user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(
                scorecard_info_by_organisation, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


#########################################Strategy Key Focus Area#############################################################


class CreateStrategyView(CreateAPIView):
    permission_classes = []
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Strategy created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Strategy, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Strategy. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllStrategies(ListAPIView):
    permission_classes = []
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()


class StrategyReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()


class StrategyUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()


class GetStrategyByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            strategy = self.queryset.filter(scorecard__user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(strategy, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllStrategiesByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = StrategySerializer
    queryset = Strategy.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            scorecard_info_by_organisation = self.queryset.filter(
                scorecard__user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(
                scorecard_info_by_organisation, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


#########################################Function Key Focus Area#############################################################


class CreateFunctionView(CreateAPIView):
    permission_classes = []
    serializer_class = FunctionSerializer
    queryset = Function.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Function created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Function, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Function. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllFunctions(ListAPIView):
    permission_classes = []
    serializer_class = FunctionSerializer
    queryset = Function.objects.all()


class FunctionReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = FunctionSerializer
    queryset = Function.objects.all()


class FunctionUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = FunctionSerializer
    queryset = Function.objects.all()


class GetFunctionByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = FunctionSerializer
    queryset = Function.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            scorecard = self.queryset.filter(scorecard__user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(scorecard, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllFunctionsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = FunctionSerializer
    queryset = Function.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            strategy_info_by_organisation = self.queryset.filter(
                scorecard__user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(strategy_info_by_organisation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


#########################################Customer Key Focus Area#############################################################


class CreateCustomerView(CreateAPIView):
    permission_classes = []
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Customer created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Customer, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Customer. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllCustomers(ListAPIView):
    permission_classes = []
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class CustomerUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class GetCustomerByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            customers = self.queryset.filter(scorecard__user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(customers, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllCustomersByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            customer_info_by_organisation = self.queryset.filter(
                scorecard__user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(customer_info_by_organisation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


#########################################Innovation Key Focus Area#############################################################


class CreateInnovationView(CreateAPIView):
    permission_classes = []
    serializer_class = InnovationSerializer
    queryset = Innovation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Innovation created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Innovation, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Innovation. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllInnovations(ListAPIView):
    permission_classes = []
    serializer_class = InnovationSerializer
    queryset = Innovation.objects.all()


class InnovationReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = InnovationSerializer
    queryset = Innovation.objects.all()


class InnovationUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = InnovationSerializer
    queryset = Innovation.objects.all()


class GetInnovationByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = InnovationSerializer
    queryset = Innovation.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            innovations = self.queryset.filter(scorecard__user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(innovations, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllInnovationsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = InnovationSerializer
    queryset = Innovation.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            innovation_info_by_organisation = self.queryset.filter(
                scorecard__user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(
                innovation_info_by_organisation, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


#########################################Operation Key Focus Area#############################################################


class CreateOperationView(CreateAPIView):
    permission_classes = []
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Operation created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create Operation, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Operation. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllOperations(ListAPIView):
    permission_classes = []
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()


class OperationReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()


class OperationUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()


class GetOperationByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            operations = self.queryset.filter(scorecard__user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(operations, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllOperationsByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            operation_info_by_organisation = self.queryset.filter(
                scorecard__user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(
                operation_info_by_organisation, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


################################ Scorecard Review ####################################################


class CreateScorecardReviewView(CreateAPIView):
    permission_classes = []
    serializer_class = ScorecardReviewSerializer
    queryset = ScorecardReview.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            try:
                scorecard = Scorecard.objects.get(pk=request.data.get("scorecard"))
            except Scorecard.DoesNotExist:
                return Response(
                    {"message": "Selected Scorecard does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            User.objects.get(pk=request.data.get("reviewer_user"))
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Scorecard Review created successfully",
                    "data": serializer.data,
                }
                print(
                    "user", scorecard.user.first_name, scorecard.user.last_name, scorecard.user.email
                )

                first_name = scorecard.user.first_name.upper()

                last_name = scorecard.user.last_name.upper()
                email = scorecard.user.email
                full_name = f"{first_name } { last_name}"

                email_subject = f"Your Scorecard Has Been Reviewed"
                email_to = email
                email_from = settings.EMAIL_HOST_USER
                email_body = (
                    f"Dear {full_name},\n\nWe are pleased to inform you that your Scorecard has been reviewed by our HR Administration Team. You can now log in to your account to view the feedback and any necessary next steps."
                    f"You can login on the PMS Platform to access your reviewed Scorecard\n\n"
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
                    "message": "Failed to create Scorecard Review, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Scorecard Review. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllScorecardReview(ListAPIView):
    permission_classes = []
    serializer_class = ScorecardReviewRetrieveSerializer
    queryset = ScorecardReview.objects.all()


class ScorecardReviewReadDestroyView(RetrieveDestroyAPIView):
    permission_classes = []
    serializer_class = ScorecardReviewRetrieveSerializer
    queryset = ScorecardReview.objects.all()


class ScorecardReviewUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = ScorecardReviewUpdateSerializer
    queryset = ScorecardReview.objects.all()


class GetScorecardReviewByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = ScorecardReviewRetrieveSerializer
    queryset = ScorecardReview.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            scorecard_review = self.queryset.filter(scorecard__user_id=user_id).order_by(
                "-date_created"
            )
            serializer = self.serializer_class(scorecard_review, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAllScorecardReviewByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = ScorecardReviewSerializer
    queryset = ScorecardReview.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            scorecard_review_info = self.queryset.filter(
                scorecard__user__organisation_id=organisation_id
            )
            serializer = self.serializer_class(
                scorecard_review_info, many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class ScorecardStatusUpdateView(UpdateAPIView):
    permission_classes = []
    serializer_class = ScorecardUpdateStatusSerializer
    queryset = Scorecard.objects.all()
