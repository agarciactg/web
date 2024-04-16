from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from web.apps.base import models as models_base
from web.apps.base.utils import StandardResultsPagination
from web.apps.enrollments.api import serializers
from web.apps.enrollments import models, exceptions, constanst
from web.apps.base.api import serializers as serializers_base
from web.apps.users import constanst as constanst_users, exceptions as exceptions_users
from web.utils.mixins import APIWithCustomerPermissionsMixin

from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi


class AcademicGroupCreateAPIView(APIWithCustomerPermissionsMixin, generics.ListAPIView):
    pagination_class = StandardResultsPagination
    serializer_class = serializers.AcademicGroupsSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para crear un grupo academico.",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.AcademicGroupsSerializer(many=False),
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
        serializer = serializers.AcademicGroupsSerializer(
            data=request.data, context={"is_create": True}
        )
        serializer.is_valid(raise_exception=True)
        academic_groups = serializer.save()
        detail = serializers.AcademicGroupsSerializer(academic_groups, many=False)
        return Response(detail.data)


class AcademicGroupsActionsAPIView(APIWithCustomerPermissionsMixin, APIView):
    """
    Endpoint to get, update and delete an AcademicGroup
    """

    pagination_class = StandardResultsPagination
    serializer_class = serializers.AcademicGroupsSerializer

    def get_objects(self, id):
        try:
            return models.AcademicGroups.objects.get(id=id)
        except models.AcademicGroups.DoesNotExist:
            raise exceptions.AcademicGroupsDoesNotExistsAPIException()

    @swagger_auto_schema(
        operation_description="Endpoint para obtener el detalle de un grupo academico por su id",
        responses={
            200: serializers.AcademicGroupsDetailSerializer(many=True),
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
                        exceptions.AcademicGroupsDoesNotExistsAPIException().get_full_details(),
                    ]
                },
            ),
        },
    )
    def get(self, request, id, format=None):
        academic_group = self.get_objects(id)
        serializer = serializers.AcademicGroupsDetailSerializer(academic_group)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Endpoint para editar el registro de un grupo academico",
        responses={
            200: serializers.AcademicGroupsDetailSerializer(many=True),
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
                description=constanst.NOT_EXIST_REGISTED_ACADEMIC_GROUPS,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        exceptions.AcademicGroupsDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def put(self, request, id, format=None):
        academic_group = self.get_objects(id)
        serializer = serializers.AcademicGroupsSerializer(
            academic_group,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            academic_group_updated = serializer.save()
            detail = serializers.AcademicGroupsDetailSerializer(academic_group_updated, many=False)
            return Response(detail.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Endpoint para desactivar un Grupo Academico",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.AcademicGroupsSerializer(many=True),
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
                description=constanst.NOT_EXIST_REGISTED_ACADEMIC_GROUPS,
                schema=serializers_base.ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        exceptions.AcademicGroupsDoesNotExistsAPIException().get_full_details()
                    ]
                },
            ),
        },
    )
    def delete(self, request, id, format=None):
        academic_group = self.get_objects(id)
        academic_group.status = models_base.BaseModel.Status.INACTIVE
        academic_group.save()
        return Response({"id": academic_group.id, "status": academic_group.status.name})


class EnrollmentCreateAPIView(APIWithCustomerPermissionsMixin, generics.ListAPIView):
    pagination_class = StandardResultsPagination
    serializer_class = serializers.EnrollmentCreateSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para crear una matricula.",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.EnrollmentCreateSerializer(many=False),
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
        serializer = serializers.EnrollmentCreateSerializer(
            data=request.data, context={"is_create": True}
        )
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()
        detail = serializers.EnrollmentCreateSerializer(enrollment, many=False)
        return Response(detail.data)

