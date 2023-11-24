from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="WEB",
        default_version="v1",
        description="API WEB",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="agarciacompanyctg@gmail.com"),
        license=openapi.License(name="Software"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.apps.base.api.urls")),
    path("", include("web.apps.users.api.urls")),
    # Temporary redirect
    path("", RedirectView.as_view(url="admin/")),
    # Documentation
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
