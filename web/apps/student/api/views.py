from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from web.apps.base.models import BaseModel
from web.apps.base.utils import StandardResultsPagination
from web.apps.student.models import Student
from web.apps.users.models import User
from web.utils.mixins import APIWithCustomerPermissionsMixin, APIWithUserPermissionsMixin
from web.apps.student.api import serializers
from web.apps.users import constanst as constanst_users, exceptions as exceptions_users
from web.apps.base.api import serializers as serializers_base
# from web.apps.users import models
# from django.db.models import Q
# from django.db.models import Q, CharField
# from django.db.models.functions import Cast

# from django.utils.decorators import method_decorator
# from django.contrib.admin.views import decorators
# from dal import autocomplete


from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2 import openapi


class AcademicGroupCreateAPIView(APIWithCustomerPermissionsMixin, generics.ListAPIView):
    pagination_class = StandardResultsPagination
    serializer_class = serializers.CandidateCreateSerializer

    @swagger_auto_schema(
        operation_description="Endpoint para crear un grupo academico.",
        request_body=serializers_base.ExceptionSerializer(many=False),
        responses={
            200: serializers.CandidateCreateSerializer(many=False),
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
        serializer = serializers.CandidateCreateSerializer(data=request.data, context={"is_create": True})
        serializer.is_valid(raise_exception=True)
        academic_groups = serializer.save()
        detail = serializers.CandidateCreateSerializer(academic_groups, many=False)
        return Response(detail.data)


class StudentUsersListAPIView(APIWithUserPermissionsMixin, generics.ListAPIView):
    serializer_class = serializers.StudentDetailSerializer
    queryset = Student.objects.all()
    pagination_class = None

    def post(self, request, *args, **kwargs):
        if not request.user:
            raise exceptions_users.UserDoesNotExistsAPIException()

        if self.request.user.type_user in [
            User.UserType.ADMIN,
            User.UserType.TEACHER,
        ]:

            students = Student.objects.filter(status=BaseModel.Status.ACTIVE).order_by("id")
            serializer = serializers.StudentDetailSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response([], status=status.HTTP_403_FORBIDDEN)


# @method_decorator([decorators.staff_member_required], name="dispatch")
# class CandidateAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         user = self.request.user
#         if not user.is_authenticated:
#             return models.User.objects.none()

#         qs = models.User.objects.all()

#         if self.q:
#             qs = qs.filter(
#                 Q(username__istartswith=self.q)
#                 | Q(first_name__istartswith=self.q)
#                 | Q(last_name__istartswith=self.q)
#                 # | Q(Cast('document_number', CharField())__istartswith=self.q)
#             )

#         return qs
