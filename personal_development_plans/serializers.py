from rest_framework.serializers import ModelSerializer
from accounts.serializers import MinimizedUserSerializer
from departments.serializers import MinimizedDepartmentSerializer
from personal_development_plans.models import Pdp, PdpReviewer



class PdpSerializer(ModelSerializer):

    class Meta:
        model = Pdp
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": True},
            "department": {"required": True},
            "career_goals": {"required": True},
            "career_journey": {"required": True},
            "skills": {"required": True},
            "opportunities": {"required": True},
            "development_goals": {"required": True},
            "work_life_balance": {"required": True},
            "personal_goals": {"required": True},
            "career_expectations": {"required": True},
        }


class PdpRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()
    department = MinimizedDepartmentSerializer()

    class Meta:
        model = Pdp
        fields = "__all__"


class PdpUpdateSerializer(ModelSerializer):

    class Meta:
        model = Pdp
        fields = "__all__"


class PdpReviewerSerializer(ModelSerializer):

    class Meta:
        model = PdpReviewer
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": True},
            "pdp": {"required": True},
            "comment": {"required": True},
            "reviewer_feedback": {"required": True},
        }


class PdpReviewerRetrieveSerializer(ModelSerializer):
    user = MinimizedUserSerializer()
   
    pdp = PdpSerializer()

    class Meta:
        model = PdpReviewer
        fields = "__all__"


class PdpReviewerUpdateSerializer(ModelSerializer):

    class Meta:
        model = PdpReviewer
        fields = "__all__"