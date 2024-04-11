from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserUserCreationForm
from django.utils.translation import gettext_lazy as _

from web.apps.users.models import User


class UserCreationForm(BaseUserUserCreationForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "type_user")
        help_texts = {
            "username": "Si el usuario es tipo administrador use email para username, de lo contrario use C.C. como username."  # noqa
        }


class UserChangeForm(BaseUserChangeForm):
    """A form for updating user. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password", "is_active")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("username", "first_name", "last_name", "document_number", "type_user", "date_joined", "is_active")
    list_filter = ("type_user",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username", "document_number")}),
        (_("Type of User"), {"fields": ("type_user",)}),
        (
            _("Admin"),
            {
                "fields": (
                    "user_permissions",
                    "groups",
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "last_login",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "type_user",
                    "first_name",
                    "last_name",
                    "type_document",
                    "document_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
    icon_name = "people"
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
