from asyncio.log import logger
from datetime import timezone
import pandas as pd
from agents.resources import AgentResource
from departments.models import Department
from organisations.models import Organisation
from .serializers import AgentSerializer, AgentRetrieveSerializer
from .models import Agent
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    GenericAPIView,
)
from rest_framework import status
from django.conf import settings
from accounts.models import User
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser
from tablib import Dataset
from rest_framework.views import APIView
from accounts.serializers import UserBulkUploadFileSerializer

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
            agent_info_by_organisation = self.queryset.filter(
                user__organisation_id=organisation_id
            )
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


class BulkUploadAgentDataView(GenericAPIView):
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserBulkUploadFileSerializer

    def post(self, request, *args, **kwargs):
        try:
            organisation = Organisation.objects.get(pk=request.data.get("organisation"))
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        file_type = request.data.get("file_type", None)
        file = request.data.get("file", None)

        if not file_type or not file:
            return Response(
                {"error": "File type and file are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        agent_resource = AgentResource()
        df = None

        try:
            if file_type == "CSV":
                try:
                    df = pd.read_csv(file)
                except Exception as e:
                    return Response(
                        {
                            "error": "Failed to read the csv file, please check the file format."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif file_type == "json":
                try:
                    df = pd.read_json(file)
                except Exception as e:
                    return Response(
                        {
                            "error": "Failed to read the json file, please check the file format."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif file_type == "XLSX" or file_type == "XLS":
                try:
                    df = pd.read_excel(file)
                except Exception as e:
                    return Response(
                        {
                            "error": "Failed to read the excel file, please check the file format."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Unsupported file type."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            dataset = Dataset().load(df)
            result = agent_resource.import_data(
                dataset, dry_run=True, raise_errors=True
            )

            if not result.has_errors():
                for row in dataset.dict:
                    try:
                        department_id = row.get("department")
                        department = (
                            Department.objects.get(
                                id=department_id, organisation_id=organisation
                            )
                            if department_id
                            else None
                        )
                    except Department.DoesNotExist:
                        return Response(
                            "Department does not exist",
                            status=status.HTTP_404_NOT_FOUND,
                        )

                    user = User.objects.create(
                        first_name=row.get("first_name"),
                        last_name=row.get("last_name"),
                        email=row.get("email"),
                        phone_number=row.get("phone_number"),
                        gender=row.get("gender"),
                        role=row.get("role"),
                        national_id=row.get("national_id"),
                        dob=row.get("dob"),
                        organisation=organisation,
                        department=department,
                        contract_tenure=row.get("contract_tenure"),
                        contract_type=row.get("contract_type"),
                        account_status=row.get("account_status"),
                        user_status=row.get("user_status"),
                        nationality=row.get("nationality"),
                        province=row.get("province"),
                        home_address=row.get("home_address"),
                        job_title=row.get("job_title"),
                        current_location=row.get("current_location"),
                        agent_type=row.get("agent_type"),
                    )
                    user.role = "AGENT"
                    new_username = f"{user.username}AG"
                    user.username = new_username
                    user.set_password("omni-Agent-123")
                    user.save()

                    Agent.objects.create(
                        user=user,
                    )

                try:
                    serializer = self.serializer_class(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                except Exception as e:
                    pass
                return Response(
                    {"message": "Agents uploaded successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"error": "Error importing data.", "details": result.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to upload agent data, an error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class AgentsGenderRatioByOrganisationIdView(GenericAPIView):
    permission_classes = []
    serializer_class = AgentRetrieveSerializer
    queryset = Agent.objects.all()

    def get(self, request, organisation_id):
        try:
            Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response("Organisation not found", status=status.HTTP_404_NOT_FOUND)
        else:
            total_agents = self.queryset.filter(user__organisation_id=organisation_id).count()
            total_male_agents = self.queryset.filter(user__gender="MALE").count()
            total_female_agents = self.queryset.filter(user__gender="FEMALE").count()

            if total_male_agents <= 0 and total_female_agents <= 0:
                return Response(
                    data={
                        "male_agents": {"total": 0, "percentage": 0},
                        "female_agents": {"total": 0, "percentage": 0},
                    },
                    status=status.HTTP_200_OK,
                )

            male_percentage = float(
                (total_male_agents / (total_male_agents + total_female_agents)) * 100
            )
            female_percentage = float(
                (total_female_agents / (total_male_agents + total_female_agents)) * 100
            )

            data = (
                {
                    "total_agents": total_agents,
                    "male_agents": {
                        "total": total_male_agents,
                        "percentage": f"{male_percentage:.2f}",
                    },
                    "female_agents": {
                        "total": total_female_agents,
                        "percentage": f"{female_percentage:.2f}",
                    },
                },
            )

            return Response(data, status=status.HTTP_200_OK)
