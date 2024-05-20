from rest_framework import serializers

from django.db.transaction import atomic

from web.apps.enrollments import models
from web.apps.teacher import models as models_teacher
from web.apps.teacher.api import serializers as serializers_teacher
from web.apps.users.api.serializers import UserDetailSummarySerializer


class AcademicGroupsSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=models_teacher.Teacher.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = models.AcademicGroups
        fields = ("teachers", "degress", "name", "code")

    def create(self, validated_data):
        with atomic():
            teachers = validated_data.pop("teachers", None)
            academic_group = models.AcademicGroups.objects.create(**validated_data)
            if teachers:
                for teacher in teachers:
                    academic_group.teachers.add(teacher)
            academic_group.save()
            return academic_group


class AcademicGroupsDetailSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        queryset=models_teacher.Teacher.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )
    # degrees = serializers.IntegerField(source="get_degrees_display")   # Corregido el nombre del campo "degrees"

    class Meta:
        model = models.AcademicGroups
        fields = ("id", "teachers", "degress", "name", "code")


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=models_teacher.Subject.objects.all(),  # Ajusta el queryset según tu modelo de Subject
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = models.Enrollment
        fields = (
            "academic_groups",
            "subjects",
            "student",
            "date_created"
        )

    def create(self, validated_data):
        with atomic():
            subjects = validated_data.pop("subjects", None)
            enrollment = models.Enrollment.objects.create(**validated_data)  # Crea un objeto Enrollment
            if subjects:
                for subject in subjects:
                    enrollment.subjects.add(subject)
            enrollment.save()
            return enrollment


class EnrollmentDetailSerializer(serializers.ModelSerializer):
    subjects = serializers_teacher.SubjectSerializer(many=True, required=False, allow_null=True)
    academic_groups = AcademicGroupsDetailSerializer()
    student = UserDetailSummarySerializer()

    class Meta:
        model = models.Enrollment
        fields = (
            "id",
            "academic_groups",
            "subjects",
            "student",
            "date_created"
        )

