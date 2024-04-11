from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView


from web.apps.base.api import serializers as serializers_base
from web.apps.base.utils import StandardResultsPagination
from web.apps.teacher import exceptions, models, constanst
from web.apps.users import constanst as constanst_users
from web.apps.users import exceptions as exceptions_users
from web.utils.mixins import APIWithCustomerPermissionsMixin
from web.apps.teacher.api import serializers
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi


class TeacherCreateAPIView(APIWithCustomerPermissionsMixin, generics.ListAPIView):
    pagination_class = StandardResultsPagination
    serializer_class = serializers.TeacherDetailSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para crear un usuario tipo docente.",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.TeacherDetailSerializer(many=False),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=constanst_users.NOT_AUTORIZATION,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": exceptions_users.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=constanst_users.NOT_EXIST_REGISTED_USER,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": exceptions_users.UserDoesNotExistsAPIException().get_full_details()
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.TeacherCreateActionSerializer(data=request.data, context={"is_create": True})
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        detail = serializers.TeacherDetailSerializer(teacher, many=False)
        return Response(detail.data)


class TeacherActionsAPIView(APIWithCustomerPermissionsMixin, APIView):
    """
    Endpoint to get, update and delete a teacher
    """

    pagination_class = StandardResultsPagination
    serializer_class = serializers.TeacherCreateActionSerializer

    def get_objects(self, id):
        try:
            return models.Teacher.objects.get(id=id)
        except models.Teacher.DoesNotExist:
            raise exceptions.TeacherDoesNotExistsAPIException()

    @swagger_auto_schema(
        operation_description="Endpoint para obtener el detalle de un docente por su id",
        responses={
            200: serializers.TeacherDetailSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=constanst_users.NOT_AUTORIZATION,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": exceptions_users.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="",
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        exceptions_users.UserDoesNotExistsAPIException().get_full_details(),
                        exceptions.TeacherDoesNotExistsAPIException().get_full_details(),
                    ]
                },
            ),
        },
    )
    def get(self, request, id, format=None):
        teacher = self.get_objects(id)
        serializer = serializers.TeacherDetailSerializer(teacher)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Endpoint para editar el registro de un docente",
        responses={
            200: serializers.TeacherCreateActionSerializer(many=True),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=constanst_users.NOT_AUTORIZATION,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": exceptions_users.UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=constanst.NOT_EXIST_REGISTED_TEACHER,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        exceptions.TeacherDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def put(self, request, id, format=None):
        teacher = self.get_objects(id)
        serializer = serializers.TeacherCreateActionSerializer(
            teacher,
            data=request.data,
            partial=True,
            context={"is_create": False, "current_user": teacher}
        )
        if serializer.is_valid():
            teacher_updated = serializer.save()
            detail = serializers.TeacherDetailSerializer(teacher_updated, many=False)
            return Response(detail.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
