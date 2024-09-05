from django.urls import path

from web.apps.student.api import views

app_name = "student_api"

urlpatterns = [
    path(
        "api/v1/student/list/",
        views.StudentUsersListAPIView.as_view(),
        name="student-list"
    )
    # path(
    #     "users_candidate_autocomplete/",
    #     views.CandidateAutocomplete.as_view(),
    #     name="candidate-select"
    # )
]
