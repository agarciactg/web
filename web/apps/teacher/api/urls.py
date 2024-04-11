from django.urls import path

from web.apps.teacher.api import views


app_name = "teacher_api"

urlpatterns = [
    path("api/v1/teacher/create/", views.TeacherCreateAPIView.as_view(), name="teacher_create"),
    path("api/v1/teacher/actions/<int:id>/", views.TeacherActionsAPIView.as_view(), name="teacher_actions"),
]
