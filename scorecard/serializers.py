from rest_framework.serializers import ModelSerializer
from .models import (
    Scorecard,
    ScorecardReview,
    ScorecardClone,
    Customer,
    Innovation,
    Function,
    Strategy,
    Operation,
)
from accounts.serializers import MinimizedUserSerializer
from django.db import transaction
from rest_framework.exceptions import ValidationError


################### Key Focus Areas ##########################
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


class OperationSerializer(ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"


################### Bulky Key Focus Areas ##########################


class StrategyBulkSerializer(ModelSerializer):
    class Meta:
        model = Strategy
        exclude = ["scorecard"]


class CustomerBulkSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = ["scorecard"]


class InnovationBulkSerializer(ModelSerializer):
    class Meta:
        model = Innovation
        exclude = ["scorecard"]


class FunctionBulkSerializer(ModelSerializer):
    class Meta:
        model = Function
        exclude = ["scorecard"]


class OperationBulkSerializer(ModelSerializer):
    class Meta:
        model = Operation
        exclude = ["scorecard"]


################### Scorecard ##########################


class ScorecardSerializer(ModelSerializer):

    class Meta:
        model = Scorecard
        exclude = ["status", "actual_score", "manager_score", "document_proof"]

        extra_kwargs = {
            "user": {"required": True},
            "name": {"required": True},
        }


class ScorecardBulkyCreateSerializer(ModelSerializer):
    strategies = StrategyBulkSerializer(many=True)
    customers = CustomerBulkSerializer(many=True)
    innovations = InnovationBulkSerializer(many=True)
    functions = FunctionBulkSerializer(many=True)
    operations = OperationBulkSerializer(many=True)

    class Meta:
        model = Scorecard
        exclude = ["status", "actual_score", "manager_score", "document_proof"]

    def create(self, validated_data):
        strategies_data = validated_data.pop("strategies", [])
        customers_data = validated_data.pop("customers", [])
        innovations_data = validated_data.pop("innovations", [])
        functions_data = validated_data.pop("functions", [])
        operations_data = validated_data.pop("operations", [])

        try:
            with transaction.atomic():
                scorecard = Scorecard.objects.create(**validated_data)

                for strategy_data in strategies_data:
                    Strategy.objects.create(scorecard=scorecard, **strategy_data)

                for customer_data in customers_data:
                    Customer.objects.create(scorecard=scorecard, **customer_data)

                for innovation_data in innovations_data:
                    Innovation.objects.create(scorecard=scorecard, **innovation_data)

                for function_data in functions_data:
                    Function.objects.create(scorecard=scorecard, **function_data)

                for operation_data in operations_data:
                    Operation.objects.create(scorecard=scorecard, **operation_data)

                return scorecard

        except Exception as e:
            if "scorecard" in locals():
                scorecard.delete()
            raise ValidationError(f"Error creating scorecard: {str(e)}")


class ScorecardRetrieveSerializer(ModelSerializer):
    strategies = StrategySerializer(many=True, read_only=True)
    customers = CustomerSerializer(many=True, read_only=True)
    innovations = InnovationSerializer(many=True, read_only=True)
    functions = FunctionSerializer(many=True, read_only=True)
    operations = OperationSerializer(many=True, read_only=True)
    user = MinimizedUserSerializer()

    class Meta:
        model = Scorecard
        fields = "__all__"


class ScorecardUpdateSerializer(ModelSerializer):

    class Meta:
        model = Scorecard
        fields = "__all__"


class ScorecardUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Scorecard
        fields = ["status"]


################### Scorecard Review##########################


class ScorecardReviewSerializer(ModelSerializer):

    class Meta:
        model = ScorecardReview
        fields = "__all__"

        extra_kwargs = {
            "scorecard": {"required": True},
            "manager_comment": {"required": True},
            "reviewer_user": {"required": True},
        }


class ScorecardReviewRetrieveSerializer(ModelSerializer):
    scorecard = ScorecardRetrieveSerializer()

    class Meta:
        model = ScorecardReview
        fields = "__all__"


class ScorecardReviewUpdateSerializer(ModelSerializer):

    class Meta:
        model = ScorecardReview
        fields = "__all__"


################### Scorecard Clone ##########################


class ScorecardCloneSerializer(ModelSerializer):

    class Meta:
        model = ScorecardClone
        fields = "__all__"

        extra_kwargs = {
            "scorecard": {"required": True},
            "recipient": {"required": True},
            "approver": {"required": True},
        }


class ScorecardCloneRetrieveSerializer(ModelSerializer):
    scorecard = ScorecardRetrieveSerializer()
    approver = MinimizedUserSerializer()
    recipient = MinimizedUserSerializer()

    class Meta:
        model = ScorecardClone
        fields = "__all__"


class ScorecardCloneUpdateSerializer(ModelSerializer):

    class Meta:
        model = ScorecardClone
        fields = "__all__"
