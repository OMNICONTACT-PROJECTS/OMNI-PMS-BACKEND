from rest_framework.serializers import ModelSerializer
from .models import (
    Scorecard,
    ScorecardReview,
    ScorecardClone,
    Customer,
    Innovation,
    Function,
    Strategy,
    Operations,
)
from accounts.serializers import UserSerializer, RetrieveUserSerializer
from accounts.models import User
from accounts.serializers import MinimizedUserSerializer


class StrategySerializer(ModelSerializer):
    class Meta:
        model = Strategy
        fields = "__all__"


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class InnovationSerializer(ModelSerializer):
    class Meta:
        model = Innovation
        fields = "__all__"


class FunctionSerializer(ModelSerializer):
    class Meta:
        model = Function
        fields = "__all__"


class OperationsSerializer(ModelSerializer):
    class Meta:
        model = Operations
        fields = "__all__"


class ScorecardSerializer(ModelSerializer):

    class Meta:
        model = Scorecard
        exclude = ["status", "actual_score", "manager_score"]

        extra_kwargs = {
            "user": {"required": True},
            "name": {"required": True},
        }


class ScorecardRetrieveSerializer(ModelSerializer):
    strategies = StrategySerializer(many=True, read_only=True)
    customers = CustomerSerializer(many=True, read_only=True)
    innovations = InnovationSerializer(many=True, read_only=True)
    functions = FunctionSerializer(many=True, read_only=True)
    operations = OperationsSerializer(many=True, read_only=True)
    user = MinimizedUserSerializer()

    class Meta:
        model = Scorecard
        fields = "__all__"




# class PdpUpdateSerializer(ModelSerializer):

#     class Meta:
#         model = Pdp
#         fields = "__all__"


# class PdpUpdateStatusSerializer(ModelSerializer):

#     class Meta:
#         model = Pdp
#         fields = []


# class PdpReviewerSerializer(ModelSerializer):

#     class Meta:
#         model = PdpReviewer
#         fields = "__all__"

#         extra_kwargs = {
#             "user": {"required": True},
#             "pdp": {"required": True},
#             "comment": {"required": True},
#             "reviewer_feedback": {"required": True},
#         }


# class PdpReviewerRetrieveSerializer(ModelSerializer):
#     user = MinimizedUserSerializer()

#     pdp = PdpSerializer()

#     class Meta:
#         model = PdpReviewer
#         fields = "__all__"


# class PdpReviewerUpdateSerializer(ModelSerializer):

#     class Meta:
#         model = PdpReviewer
#         fields = "__all__"
