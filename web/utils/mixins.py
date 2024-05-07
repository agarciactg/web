from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey


class APIBasePermissionsMixin:
    permission_classes = [IsAdminUser | HasAPIKey]


class APIWithUserPermissionsMixin:
    permission_classes = [IsAuthenticated & HasAPIKey]


class APIWithCustomerPermissionsMixin:
    permission_classes = [IsAuthenticated | HasAPIKey]
