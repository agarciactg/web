from django.db.transaction import atomic
from rest_framework import serializers

from web.apps.base import models as models_base
from web.apps.teacher import models
from web.apps.teacher import exceptions
from web.apps.users import models as models_users
from web.apps.users.api import serializers as serializers_user


class TeacherDetailSerializer(serializers.ModelSerializer):
    user = serializers_user.UserDetailSummarySerializer(many=False)

    class Meta:
        model = models.Teacher
        fields = ("id", "uuid", "user", "profession", "is_full_time")


class TeacherCreateActionSerializer(serializers.Serializer):
    """
    Serializer to create and update a teacher
    """

    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, max_length=250, required=True)
    type_document = serializers.IntegerField(write_only=True)
    document_number = serializers.IntegerField(write_only=True)
    avatar = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    avatar_url = serializers.URLField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True)
    city = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=models_base.City.objects.filter(status=models_base.BaseModel.Status.ACTIVE),
        allow_null=True,
        required=False,
    )
    profession = serializers.CharField(write_only=True, required=False)
    is_full_time = serializers.BooleanField(write_only=True, required=False, default=False)

    def validate(self, attrs):
        data = super().validate(attrs)

        if self.context["is_create"]:
            if (
                models_users.User.objects.filter(username=data["username"]).exists()
                or models.Teacher.objects.filter(
                    user__document_number=data["document_number"]
                ).exists()
            ):
                raise exceptions.TeacherAlreadyExistsException()
        else:

            current_teacher = self.context["current_user"]
            if (
                current_teacher.user.document_number != data.get("document_number")
                or current_teacher.user.username != data.get("username")
            ) and (
                models_users.User.objects.filter(username=data.get("username"))
                .exclude(id=current_teacher.user.id)
                .exists()
            ):
                if "document_number" in data:
                    if (
                        models.Teacher.objects.filter(document_number=data.get("document_number"))
                        .exclude(id=current_teacher.id)
                        .exists()
                    ):
                        raise exceptions.TeacherAlreadyExistsException()

                raise exceptions.TeacherAlreadyExistsException()

        return data

    def create(self, validated_data):
        with atomic():
            user_data = {
                "username": validated_data.pop("username"),
                "type_user": models_users.User.UserType.TEACHER,
                "first_name": validated_data.pop("first_name"),
                "last_name": validated_data.pop("last_name"),
                "type_document": validated_data.pop("type_document"),
                "document_number": validated_data.pop("document_number"),
                "email": validated_data.pop("email"),
                "avatar": validated_data.pop("avatar", None),
                "avatar_url": validated_data.pop("avatar_url", None),
            }

            # Save the information of the user
            user = models_users.User.objects.create(**user_data)
            user.set_password(str(validated_data.pop("password")))
            user.save()

            teacher_data = {
                "profession": validated_data.get("profession", None),
                "is_full_time": validated_data.get("is_full_time"),
            }

            teacher = models.Teacher.objects.create(user=user, **teacher_data)
        return teacher

    def update(self, teacher, validated_data):
        with atomic():
            user = teacher.user
            user.username = validated_data.get("username", user.username)
            user.first_name = validated_data.get("first_name", user.first_name)
            user.last_name = validated_data.get("last_name", user.last_name)
            user.type_document = validated_data.get("type_document", user.type_document)
            user.document_number = validated_data.get("document_number", user.document_number)
            user.email = validated_data.get("email", user.email)
            user.avatar = validated_data.get("avatar", user.avatar)
            user.avatar_url = validated_data.get("avatar_url", user.avatar_url)

            password = validated_data.pop("password", None)
            if password:
                user.set_password(str(password))
            user.save()

            teacher.profession = validated_data.get("profession", teacher.profession)
            teacher.is_full_time = validated_data.get("is_full_time", teacher.is_full_time)
            teacher.save()

            return teacher


class SubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=models.Teacher.objects.all(),
        write_only=True  # Esto asegura que el campo no se incluya al serializar
    )

    class Meta:
        model = models.Subject
        fields = ("teacher", "name", "description", "credis", "hours")
