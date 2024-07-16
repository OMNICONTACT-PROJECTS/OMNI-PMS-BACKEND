<<<<<<< HEAD:subscribers/views.py
import pandas as pd
from organisations.models import Organisation
from subscribers.resources import SubscriberResource
from .serializers import SubscriberFileSerializer, SubscriberSerializer, SubscriberRetrieveSerializer
from .models import Subscriber
=======
from .serializers import AgentSerializer, AgentRetrieveSerializer
from .models import Agent
>>>>>>> 4554fa613482b9478d4c44efc35b9a1d863dae26:agents/views.py
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
<<<<<<< HEAD:subscribers/views.py
    serializer_class = SubscriberRetrieveSerializer
    queryset = Subscriber.objects.all()


class BulkUploadSubscriberDataView(GenericAPIView):
    permission_classes = []
    serializer_class = SubscriberFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            Organisation.objects.get(pk=request.data.get("organisation"))
        except Organisation.DoesNotExist:
            return Response(
                {"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            try:
                file_type = request.data.get("file_type", None)
                file = request.data.get("file", None)

                if not file_type or not file:
                    return Response(
                        {"error": "File type and file are required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                subscriber_resource = SubscriberResource()
                df = None

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
                try:
                    result = subscriber_resource.import_data(
                        dataset, dry_run=True, raise_errors=True
                    )
                except Exception as e:
                    error_message = str(e)
                    error_index = error_message.find("]")
                    if error_index != -1:
                        error_message = error_message[: error_index + 1]
                    return Response(
                        {
                            "message": "Failed to upload Subscriber data, here an error occurred",
                            "error": error_message,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not result.has_errors():
                    subscriber_resource.import_data(dataset, dry_run=False)
                    try:

                        
                        
                        serializer = self.serializer_class(data=request.data)
                        if serializer.is_valid():
                            saved_instance = serializer.save()
                            # # saved_instance.campaign_name = "Sasai Campaign"
                            saved_instance.save()
                        
                            pass
                            
                    except Exception as e:
                        pass
                    return Response(
                        {"message": "Subscriber Data Uploaded Successfully."},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"error": "Error importing data."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                return Response(
                    {
                        "message": "Failed to upload Subscriber data, an error occurred",
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


class GetAllSubscriberByOrganisationId(GenericAPIView):
    permission_classes = []
    serializer_class = SubscriberRetrieveSerializer
    queryset = Subscriber.objects.all()

    def get(self, request, organisation_id):
        try:
            organisation = Organisation.objects.get(pk=organisation_id)
        except Organisation.DoesNotExist:
            return Response(
                data={"message": "Organisation does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            subscriber_info_by_organisation = self.queryset.filter(user__organisation_id=organisation_id)
            serializer = self.serializer_class(subscriber_info_by_organisation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
=======
    serializer_class = AgentRetrieveSerializer
    queryset = Agent.objects.all()
>>>>>>> 4554fa613482b9478d4c44efc35b9a1d863dae26:agents/views.py
