from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

    class Meta:
        model = models.User
        fields = (
            "id",
            "type_user",
            "first_name",
            "last_name",
            "username",
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
        )


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
    password = serializers.CharField()
    confirm_password = serializers.CharField()
