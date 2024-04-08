from django.conf import settings

from django.contrib.admin import ModelAdmin, register

from web.apps.teacher import models


@register(models.Teacher)
class TeacherAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "profession",
        "is_full_time",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "school"

    def get_full_name(self, obj):
        return obj.user.get_full_name()


@register(models.Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ("id", "teacher", "name", "credis", "hours")
    search_fields = (
        "teacher__user__username",
        "teacher__user__first_name",
        "teacher__user__last_name",
    )
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "storage"

    def get_full_name(self, obj):
        return obj.user.get_full_name()
