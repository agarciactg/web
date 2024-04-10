from django.conf import settings
from django.contrib.admin import ModelAdmin, register

from web.apps.enrollments import models
from web.apps.users import models as models_users


@register(models.Enrollment)
class EnrollmentsAdmin(ModelAdmin):
    list_display = (
        "id",
        "student",
        "date_created",
    )
    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
    )
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "collections_bookmark"

    fields = ["academic_groups", "subjects", "student"]

    # Default: return only user type student in enrollment
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = models_users.User.objects.filter(
                type_user=models_users.User.UserType.STUDENT
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@register(models.AcademicGroups)
class AcademicGroupsAdmin(ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "degress"
    )
    search_fields = (
        "name",
        "code",
        "degress"
    )
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "group_work"
