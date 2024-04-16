from django.urls import path
from web.apps.enrollments.api import views

app_name = "enrollments_api"

urlpatterns = [
    path(
        "api/v1/academic_group/create/",
        views.AcademicGroupCreateAPIView.as_view(),
        name="academic_group_create",
    ),
    path(
        "api/v1/academic_group/actions/<int:id>/",
        views.AcademicGroupsActionsAPIView.as_view(),
        name="academic_group_update",
    ),
    path(
        "api/v1/enrollment/create/",
        views.EnrollmentCreateAPIView.as_view(),
        name="enrollment_group_create",
    ),
]
