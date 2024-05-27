from django.urls import path

from web.apps.teacher.api import views


app_name = "teacher_api"

urlpatterns = [
    path("api/v1/teacher/create/", views.TeacherCreateAPIView.as_view(), name="teacher_create"),
    path("api/v1/teacher/actions/<int:id>/", views.TeacherActionsAPIView.as_view(), name="teacher_actions"),
    path("api/v1/subject/create/", views.SubjectsCreateAPIView.as_view(), name="subjects_create"),
    path("api/v1/subject/actions/<int:id>/", views.SubjectActionsAPIView.as_view(), name="subjects_actions"),
    path("api/v1/subject/list/", views.SubjectsAPIView.as_view(), name="subjects_list"),
    path("api/v1/teachers/list/", views.TeachersAPIView.as_view(), name="teacher_list"),

]
