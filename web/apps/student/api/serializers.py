from rest_framework import serializers
from web.apps.student import models
from web.apps.users.api.serializers import UserDetailSummarySerializer
from web.apps.users.models import User


class CandidateCreateSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), many=False, required=True
    )
    gender = serializers.SerializerMethodField()
    laterality = serializers.SerializerMethodField()
    degrees = serializers.SerializerMethodField()

    class Meta:
        model = models.Candidate
        fields = (
            "id",
            "user",
            "place_of_bird",
            "date_of_bird",
            "years",
            "gender",
            "laterality",
            "degrees",
            "elective_year",
            "address",
            "city",
            "neighborhood",
            "stratum",
            "phone",
            "email",
        )


class CandidateDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSummarySerializer(many=False)

    class Meta:
        model = models.Candidate
        fields = (
            "id",
            "user",
            "place_of_bird",
            "date_of_bird",
            "years",
            "gender",
            "laterality",
            "degrees",
            "elective_year",
            "address",
            "city",
            "neighborhood",
            "stratum",
            "phone",
            "email",
        )
