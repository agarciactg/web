from django.urls import path

from web.apps.users.api import views


app_name = "user_api"

urlpatterns = [
    path("api/v1/auth/token/", views.TokenObtainPairView.as_view(), name="token"),
    path("api/v1/auth/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/v1/auth/user/detail/",
        views.UserDetailView.as_view(),
        name="user_detail",
    ),
    path("api/v1/reset-password/", views.PasswordResetRequestView.as_view(), name="reset_password"),
    path(
        "api/v1/reset-password/confirm/<str:uidb64>/<str:token>/",
        views.passwordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path("api/v1/users/detail/", views.UserDetailAPIView.as_view(), name="user_detail"),
    path("api/v1/users/actions/<int:pk>/", views.UserActionsAPIView.as_view(), name="user_actions"),
    path("api/v1/users/create/", views.UserCreateAPIView.as_view(), name="user_create"),
]
