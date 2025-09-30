from rest_framework import serializers
from api.models import Member


class MemberSerializer(serializers.ModelSerializer):
    is_birthday_today = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = "__all__"

    def get_is_birthday_today(self, obj):
        return obj.is_birthday_today()