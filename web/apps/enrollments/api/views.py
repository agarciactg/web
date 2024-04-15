from rest_framework import generics
from rest_framework.response import Response

from web.apps.base.utils import StandardResultsPagination
from web.apps.enrollments.api import serializers
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
