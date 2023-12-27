from django.urls import include, path

from web.apps.users.api import views
from django.contrib.auth import views as auth_views


app_name = "user_api"

urlpatterns = [
    path("api/v1/auth/token/", views.TokenObtainPairView.as_view(), name="token"),
    path("api/v1/auth/token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/v1/auth/user/detail/",
        views.UserDetailView.as_view(),
        name="user_detail",
    ),
    # path(
    #     "api/v1/auth/user/change_password/<int:pk>/",
    #     views.ChangePasswordView.as_view(),
    #     name="change_password",
    # ),
    # path("api/v1/password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("api/v1/reset-password/", views.PasswordResetRequestView.as_view(), name="reset_password"),
    path(
        "api/v1/reset-password/confirm/<str:uidb64>/<str:token>/",
        views.passwordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    path("api/v1/users/detail/", views.UserDetailAPIView.as_view(), name="user_detail"),
    path("api/v1/users/actions/<int:pk>/", views.UserActionsAPIView.as_view(), name="user_actions"),
    # path("api/v1/password-reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
]
