from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView


from web.apps.base.api import serializers as serializers_base
from web.apps.base import models as models_base
from web.apps.base.utils import StandardResultsPagination
from web.apps.teacher import exceptions, models, constanst
from web.apps.users import constanst as constanst_users, exceptions as exceptions_users
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

    @swagger_auto_schema(
        operation_description="Endpoint para desactivar un Profesor",
        request_body=serializers_base.ExceptionSerializer(many=False),
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
    def delete(self, request, id, format=None):
        teacher = self.get_objects(id)
        teacher.status = models_base.BaseModel.Status.INACTIVE
        teacher.save()
        return Response({"id": teacher.id, "status": teacher.status.name})


class SubjectsCreateAPIView(APIWithCustomerPermissionsMixin, generics.ListAPIView):
    pagination_class = StandardResultsPagination
    serializer_class = serializers.SubjectSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para crear una Asignatura.",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.SubjectSerializer(many=False),
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
        serializer = serializers.SubjectSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()
        detail = serializers.SubjectSerializer(subject, many=False)
        return Response(detail.data)


class SubjectActionsAPIView(APIWithCustomerPermissionsMixin, APIView):
    pagination_class = StandardResultsPagination
    serializer_class = serializers.SubjectSerializer

    def get_objects(self, id):
        try:
            return models.Subject.objects.get(id=id)
        except models.Subject.DoesNotExist:
            raise exceptions.SubjectsDoesNotExistsAPIException()

    @swagger_auto_schema(
        operation_description="Endpoint para obtener el detalle de una asignatura.",
        responses={
            200: serializers.SubjectSerializer(many=True),
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
                        exceptions.SubjectsDoesNotExistsAPIException().get_full_details(),
                    ]
                },
            ),
        },
    )
    def get(self, request, id, format=None):
        teacher = self.get_objects(id)
        serializer = serializers.SubjectSerializer(teacher)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Endpoint para editar el registro una Asignatura",
        responses={
            200: serializers.SubjectSerializer(many=True),
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
                        exceptions.SubjectsDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def put(self, request, id, format=None):
        subject = self.get_objects(id)
        serializer = serializers.SubjectSerializer(
            subject,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            subject_update = serializer.save()
            detail = serializers.SubjectSerializer(subject_update, many=False)
            return Response(detail.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Endpoint para desactivar una asignatura",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.SubjectSerializer(many=True),
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
                description=constanst.NOT_EXIST_REGISTED_SUBJECTS,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        exceptions.SubjectsDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def delete(self, request, id, format=None):
        subject = self.get_objects(id)
        subject.status = models_base.BaseModel.Status.INACTIVE
        subject.save()
        return Response({"id": subject.id, "status": subject.status.name})
