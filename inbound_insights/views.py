from .serializers import VoiceInsightsSerializer, VoiceInsightsRetrieveSerializer
from .models import VoiceInsights
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework import status


# voice insights code now in voice_insights
class CreateVoiceInsightsView(CreateAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsSerializer
    queryset = VoiceInsights.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "VoiceInsights created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create voice insights, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create Voice Insights. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllVoiceInsights(ListAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()


class VoiceInsightsReadUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()
