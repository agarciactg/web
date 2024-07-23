from django.urls import path


from web.apps.tutor.api import views


app_name = "inscription_api"

urlpatterns = [
    path(
        "api/v1/inscription/create/",
        views.IncriptionCreateAPIView.as_view(),
        name="inscription_create",
    ),
]
