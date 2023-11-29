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
    path('api/v1/auth/user/change_password/<int:pk>/', views.ChangePasswordView.as_view(), name="change_password"),
    path("api/v1/password/reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("api/v1/users/detail/", views.UserDetailAPIView.as_view(), name="user_detail"),
    path("api/v1/users/actions/<int:pk>/", views.UserActionsAPIView.as_view(), name="user_actions"),
]
