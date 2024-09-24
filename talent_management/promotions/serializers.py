from ..models import Promotion
from rest_framework.serializers import ModelSerializer
from accounts.serializers import MinimizedUserSerializer


class PromotionSerializer(ModelSerializer):

    class Meta:
        model = Promotion
        fields = "__all__"


class RetrievePromotionSerializer(ModelSerializer):
    user = MinimizedUserSerializer()

    class Meta:
        model = Promotion
        fields = "__all__"


class PromotionStatusSerializer(ModelSerializer):

    class Meta:
        model = Promotion
        fields = ["status"]
