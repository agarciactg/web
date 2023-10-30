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


from web.apps.users.api import serializers
from web.apps.users import models
from web.apps.users import exceptions as users_exceptions
from web.utils import mixins


class UserDetailView(mixins.APIBasePermissionsMixin, generics.RetrieveAPIView):
    """
    return:: detail of user
    """

    serializer_class = serializers.UserDetailSerializer()
    queryset = models.User.objects.all()
    pagination_class = None

    def get(self, *args, **kwargs):
        if not self.request.user:
            raise users_exceptions.UserDoesNotExistsAPIException()

        user = models.User.objects.filter(username=self.request.user.username)
        if not user:
            raise users_exceptions.UserDoesNotExistsAPIException()

        serializer = serializers.UserDetailSerializer(self.request.user)

        return Response(data=serializer.data)


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
                return render(request, './reset_password.html',)
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
