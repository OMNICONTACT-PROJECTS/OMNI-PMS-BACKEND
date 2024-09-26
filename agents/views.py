from organisations.models import Organisation
from .serializers import AgentSerializer, AgentRetrieveSerializer
from .models import Agent
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    GenericAPIView
)
from rest_framework import status
from django.conf import settings
from accounts.models import User
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
from tablib import Dataset

# Create your views here.


class CreateAgentView(CreateAPIView):
    permission_classes = []
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Agent created successfully",
                    "data": serializer.data,
                }

                first_name = serializer.validated_data["user"]["first_name"].upper()
                last_name = serializer.validated_data["user"]["last_name"].upper()
                # username = serializer.validated_data['user']['username']
                email = serializer.validated_data["user"]["email"]
                full_name = f"{first_name } { last_name}"
                password = "omni-Agent-123"

                this_instance = User.objects.get(pk=serializer.data["user"]["id"])
                username = this_instance.username
                role = this_instance.role

                email_subject = f"Welcome to the OMNI PMS SYSTEM, Your Agent Account has been Created Successfully"
                email_to = email
                email_from = settings.EMAIL_HOST_USER
                email_body = (
                    f"Dear {full_name},\n\nWe are delighted to inform you that your account has been successfully created for the OMNI PMS SYSTEM. "
                    f"You can now access your account using the following details:\n\n"
                    f"Username: {username}\n"
                    f"Password: {password}\n"
                    f"Email: {email}\n"
                    f"Role: {role}\n\n"
                    f"Kindly use the Username and password above to Sign in to your account. \n \n"
                    f"Please keep this information secure and do not share it with anyone. If you have any questions or need assistance, "
                    f"feel free to reach out to our support team at support@omnicontact.biz.\n\n"
                    f"Thank you for joining OMNI PMS SYSTEM. We look forward to providing you with a great experience!\n\n"
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
                    "message": "Failed to create agent, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create agent. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllAgents(ListAPIView):
    permission_classes = []
    serializer_class = AgentRetrieveSerializer
    queryset = Agent.objects.all()


class AgentReadUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = AgentRetrieveSerializer
    queryset = Agent.objects.all()


class GetAllAgentByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = AgentRetrieveSerializer
    queryset = Agent.objects.all()

    def get(self, request, organisation_id):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            agent_info_by_organisation = self.queryset.filter(user__organisation_id=organisation_id)
            serializer = self.serializer_class(agent_info_by_organisation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllAgentByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = AgentRetrieveSerializer
    queryset = Agent.objects.all()

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            agent_info_by_user_id = (self.queryset.filter(user__id=user_id)).first()
            serializer = self.serializer_class(agent_info_by_user_id)
            return Response(serializer.data, status=status.HTTP_200_OK)