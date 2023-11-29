from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render

from web.apps.base.api import serializers as base_serializer
from web.apps.users.api import serializers
from web.apps.users import models
from web.apps.users import exceptions as user_exceptions
from web.apps.users import constanst as user_constants
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


class ChangePasswordView(mixins.APIBasePermissionsMixin, generics.UpdateAPIView):
    queryset = models.User.objects.all()
    permission_class = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer


class PasswordResetView(mixins.APIBasePermissionsMixin, APIView):
    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = models.User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                token = token.replace("/", "_").replace("+", "-")
                current_site = get_current_site(request)
                mail_subject = "Recuperación de contraseña"
                return render(
                    request,
                    "./reset_password.html",
                )
                # message = render_to_string(
                #     "web/templates/reset_password.html",
                #     {
                #         "user": user,
                #         "domain": current_site.domain,
                #         "uid": uid,
                #         "token": token,
                #     },
                # )
                # send_mail(mail_subject, message, "cajolod623@wanbeiz.com", [email])
                # return Response(
                #     {"message": "Correo de recuperación enviado"}, status=status.HTTP_200_OK
                # )
            else:
                return Response(
                    {"message": "Correo no encontrado"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


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
