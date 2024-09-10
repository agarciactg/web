from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


from web.apps.base.api.serializers import CitySerializer, ExceptionSerializer, GetCountMainModelsSerializer, TypeDocumentSerializer
from web.apps.base.models import BaseModel, City, TypeDocument
from web.apps.base.utils import StandardResultsPagination
from web.apps.enrollments.models import AcademicGroups, Enrollment
from web.apps.teacher.models import Subject
from web.apps.users.constanst import NOT_AUTORIZATION
from web.apps.users.exceptions import UserDoesNotExistsAPIException, UserUnauthorizedAPIException
from web.apps.users.models import User
from web.utils.mixins import APIBasePermissionsMixin, APIWithCustomerPermissionsMixin

from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi


# Api of  City
class CityAPIView(APIBasePermissionsMixin, ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.activos()
    pagination_class = StandardResultsPagination


# Api of  Type Documents
class TypeDocumentAPIView(APIBasePermissionsMixin, ListAPIView):
    serializer_class = TypeDocumentSerializer
    queryset = TypeDocument.objects.activos()
    pagination_class = StandardResultsPagination


class GetCountMainModelAPIView(APIWithCustomerPermissionsMixin, APIView):
    """
    View to get total of main models.
    """

    pagination_class = None
    serializer_class = GetCountMainModelsSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para obtener el detalle de un enrollments por su id",
        responses={
            200: GetCountMainModelsSerializer(many=False),
            401: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description=NOT_AUTORIZATION,
                schema=ExceptionSerializer(many=False),
                examples={
                    "application/json": UserUnauthorizedAPIException().get_full_details()
                },
            ),
            404: openapi.Response(
                type=openapi.TYPE_OBJECT,
                description="",
                schema=ExceptionSerializer(many=False),
                examples={
                    "application/json": [
                        UserDoesNotExistsAPIException().get_full_details(),
                    ]
                },
            ),
        },
    )
    def get(self, request, format=None):
        users = User.objects.filter(is_active=True).count()
        subjects = Subject.objects.filter(status=BaseModel.Status.ACTIVE).count()
        academics = AcademicGroups.objects.filter(status=BaseModel.Status.ACTIVE).count()
        enrollments = Enrollment.objects.filter(status=BaseModel.Status.ACTIVE).count()

        data = {
            "all_users": users,
            "all_subjects": subjects,
            "all_academic": academics,
            "all_enrollment": enrollments
        }
        return Response(data)
