from django.urls import path

from web.apps.users.api import views


app_name = "user_api"

urlpatterns = [
    path(
        "api/v1/auth/user/detail/",
        views.UserDetailView.as_view(),
        name="user_detail",
    ),
    path('api/v1/auth/user/change_password/<int:pk>/', views.ChangePasswordView.as_view(), name="change_password"),
    path("api/v1/password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
]
