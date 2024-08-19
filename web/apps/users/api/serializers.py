from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db.transaction import atomic

from web.apps.users import models


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)  # comment out if you don't want this
        data["access"] = str(refresh.access_token)
        data["type_user"] = self.user.get_type_user_display()

        return data


class SerializerTokenAuth(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)
    type_user = serializers.CharField(required=False)


class UserDetailSerializer(serializers.ModelSerializer):
    type_user = serializers.CharField(source="get_type_user_display")
    type_document = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            "id",
            "type_user",
            "first_name",
            "last_name",
            "username",
            "type_document",
            "document_number",
            "email",
            "avatar",
            "avatar_url",
            "is_active",
        )

    def get_type_document(self, obj):
        return obj.get_type_document_display()


class UserUpdatedPersonalSerializer(serializers.ModelSerializer):
    """
    Return: Serializer for updated User
    """

    type_user = serializers.ChoiceField(choices=models.User.UserType.choices)
    type_document = serializers.ChoiceField(choices=models.User.TypeDocument.choices)

    class Meta:
        model = models.User
        fields = (
            "username",
            "type_user",
            "first_name",
            "last_name",
            "type_document",
            "document_number",
            "email",
            "avatar",
            "avatar_url",
        )


class UserDetailTypeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            "id",
            "type_user",
            "first_name",
            "last_name",
            "username",
            "type_document",
            "document_number",
            "email",
            "avatar",
            "avatar_url",
            "is_active",
        )


class UserDetailSummarySerializer(serializers.ModelSerializer):
    type_user = serializers.CharField(source="get_type_user_display")

    class Meta:
        model = models.User
        fields = (
            "id",
            "type_user",
            "first_name",
            "last_name",
            "type_document",
            "document_number",
            "get_full_name"
        )

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        data = super().validate(attrs)
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match password."}
            )

        return data

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True)


class UserUpdatedPersonalSettingsSerializer(serializers.ModelSerializer):
    """
    Return: Serializer for created User
    """

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Return: Serializer for created User
    """

    type_user = serializers.ChoiceField(choices=models.User.UserType.choices)
    type_document = serializers.ChoiceField(choices=models.User.TypeDocument.choices)

    class Meta:
        model = models.User
        fields = (
            "username",
            "type_user",
            "first_name",
            "last_name",
            "type_document",
            "document_number",
            "email",
            "avatar",
            "avatar_url",
        )

    def create(self, validated_data):
        with atomic():
            type_user = validated_data.pop("type_user", None)
            type_document = validated_data.pop("type_document", None)
            user = models.User.objects.create(
                type_user=type_user, type_document=type_document, **validated_data
            )
            return user
