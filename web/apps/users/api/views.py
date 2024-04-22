import os
from django.core.mail import EmailMessage
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string

from web.apps.base.api import serializers as base_serializer
from web.apps.base.utils import StandardResultsPagination
from web.apps.users.api import serializers
from web.apps.users import models
from web.apps.users import exceptions as user_exceptions
from web.apps.users import constanst as user_constants
from web.config.settings.base import BASE_DIR
from web.utils import mixins


class TokenObtainPairView(mixins.APIWithCustomerPermissionsMixin, TokenViewBase):
    """
    Return JWT tokens (access and refresh) for specific user based on username and password.
    """

    serializer_class = serializers.UserTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para obtener un token.",
        request_body=base_serializer.ExceptionSerializer(many=False),
        responses={
            200: serializers.SerializerTokenAuth(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene Autorización.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene registro del Usuario.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserDoesNotExistsAPIException().get_full_details()
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(mixins.APIWithCustomerPermissionsMixin, TokenViewBase):
    """
    Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """

    serializer_class = TokenRefreshSerializer


class UserDetailView(mixins.APIBasePermissionsMixin, generics.RetrieveAPIView):
    """
    return:: detail of user
    """

    serializer_class = serializers.UserDetailSerializer()
    queryset = models.User.objects.all()
    pagination_class = None

    @swagger_auto_schema(
        operation_description="Endpoint para obtener el detalle de un docente por su id",
        responses={
            200: serializers.UserDetailSerializer(many=False),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=user_constants.NOT_AUTORIZATION,
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        user_exceptions.UserDoesNotExistsAPIException().get_full_details(),
                    ]
                },
            ),
        },
    )
    def get(self, *args, **kwargs):
        if not self.request.user:
            raise user_exceptions.UserDoesNotExistsAPIException()

        serializer = serializers.UserDetailSerializer(self.request.user)
        return Response(data=serializer.data)


class UserActionsAPIView(mixins.APIWithCustomerPermissionsMixin, APIView):
    """
    Endpoint to desactivate an user
    """

    serializer_class = serializers.UserDetailSerializer

    def get_objects(self, pk):
        try:
            return models.User.objects.get(id=pk)
        except models.User.DoesNotExist:
            raise user_exceptions.UserDoesNotExistsAPIException()

    @swagger_auto_schema(
        operation_description="Endpoint para obtener el detalle de una usuario.",
        responses={
            200: serializers.UserDetailSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=user_constants.NOT_AUTORIZATION,
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=user_constants.NOT_EXIST_REGISTED_USER,
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        user_exceptions.UserDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def get(self, request, pk, format=None):
        user = self.get_objects(pk)
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Endpoint para actualizar una institucion",
        request_body=base_serializer.ExceptionSerializer(many=False),
        responses={
            200: serializers.UserDetailSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        user_exceptions.UserDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def put(self, request, pk, format=None):
        user = self.get_objects(pk)
        serializer = serializers.UserDetailSerializer(
            user, data=request.data, partial=True, context={}
        )
        if serializer.is_valid(raise_exception=True):
            user_updated = serializer.save()
            detail = serializers.UserDetailSerializer(user_updated, many=False)
            return Response(detail.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Endpoint para desactivar un usuario.",
        responses={
            200: serializers.UserDetailSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene Autorización.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No existe registro del Usuario",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        user_exceptions.UserDoesNotExistsAPIException().get_full_details(),
                    ]
                },
            ),
        },
    )
    def delete(self, request, pk, format=None):
        user = self.get_objects(pk)
        if self.request.user.type_user == models.User.UserType.ADMIN:
            user.is_active = False
            user.save()
            detail = serializers.UserDetailSerializer(user, many=False)
            return Response(detail.data)

        return Response(
            {"message": "Solo el administrador puede eliminar un usuario"},
            status=status.HTTP_403_FORBIDDEN,
        )


class ChangePasswordView(mixins.APIBasePermissionsMixin, generics.UpdateAPIView):
    """
    View to change password of a user
    """
    queryset = models.User.objects.all()
    permission_class = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class PasswordResetRequestView(mixins.APIWithCustomerPermissionsMixin, APIView):
    """
    Reset password reset request with email.
    """
    @swagger_auto_schema(
        operation_description="Endpoint para restablecer contraseña via email.",
        request_body=base_serializer.ExceptionSerializer(many=False),
        responses={
            200: serializers.PasswordResetSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene Autorización.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene registro del Usuario.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserDoesNotExistsAPIException().get_full_details()
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = models.User.objects.filter(email=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            uidb64 = user.uuid
            token = token_generator.make_token(user)

            reset_url = f"{request.build_absolute_uri()}confirm/{uidb64}/{token}/"

            # template message
            email_body = render_to_string(
                os.path.join(BASE_DIR, "templates") + "/reset_password.html",
                {"user": user, "reset_url": reset_url},
            )

            mail = EmailMessage(
                "Restablecimiento de Contraseña", email_body, "agarciacompanyctg@gmail.com", [email]
            )
            mail.content_subtype = "html"
            mail.send()
            return Response(
                {"detail": "Enlace de restablecimiento enviado correctamente."},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"error": "No existe un usuario con este correo electrónico."},
                status=status.HTTP_404_NOT_FOUND,
            )


class passwordResetConfirmView(mixins.APIWithCustomerPermissionsMixin, APIView):
    @swagger_auto_schema(
        operation_description="Endpoint para cambiar la contrase segun el acceso del email.",
        request_body=base_serializer.ExceptionSerializer(many=False),
        responses={
            200: serializers.SetPasswordSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene Autorización.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="No tiene registro del Usuario.",
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserDoesNotExistsAPIException().get_full_details()
                },
            ),
        },
    )
    def post(self, request, uidb64, token):
        user = models.User.objects.filter(uuid=uidb64).first()

        if user and PasswordResetTokenGenerator().check_token(user, token):
            serializer = serializers.SetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            new_password = serializer.validated_data["password"]
            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Contraseña restablecida correctamente."}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"error": "Enlace de restablecimiento no válido."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetailAPIView(mixins.APIBasePermissionsMixin, generics.RetrieveAPIView):
    """
    Return: User Detail
    """

    serializer_class = serializers.UserDetailSerializer
    queryset = models.User.objects.all()
    pagination_class = None

    def get(self, *args, **kwargs):
        if not self.request.user:
            raise user_exceptions.UserDoesNotExistsAPIException()

        serializer = serializers.UserDetailSerializer(self.request.user)
        return Response(data=serializer.data)


class UserCreateAPIView(mixins.APIWithCustomerPermissionsMixin, generics.ListAPIView):
    """
    Return: Create User
    """

    serializer_class = serializers.UserCreateSerializer
    pagination_class = StandardResultsPagination

    @swagger_auto_schema(
        operation_description="Endpoint para crear un Usuario.",
        request_body=base_serializer.ExceptionSerializer(many=False),
        responses={
            200: serializers.UserCreateSerializer(many=False),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=user_constants.NOT_AUTORIZATION,
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=user_constants.NOT_EXIST_REGISTED_USER,
                schema=base_serializer.ExceptionSerializer(many=False),
                examples={
                    "application/json": user_exceptions.UserDoesNotExistsAPIException().get_full_details()
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(
            data=request.data, context={"is_create": True}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        detail = serializers.UserDetailSerializer(user, many=False)
        return Response(detail.data)
