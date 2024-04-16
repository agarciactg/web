from rest_framework import serializers

from django.db.transaction import atomic

from web.apps.enrollments import models
from web.apps.teacher import models as models_teacher


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
        fields = ("teachers", "degress", "name", "code")
