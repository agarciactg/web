from django.urls import path

from web.apps.base import views

app_name = "base"

urlpatterns = [
    path("status/", views.status_check, name="status_check"),
]
