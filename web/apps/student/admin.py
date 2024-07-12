from django.conf import settings
from django.contrib.admin import ModelAdmin, register

from web.apps.student import models


@register(models.Candidate)
class CandidateAdmin(ModelAdmin):
    list_display = ("id", "user", "place_of_bird", "status")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "thumbs_up_down"
    fields = [
        "user",
        "place_of_bird",
        "date_of_bird",
        "years",
        "gender",
        "laterality",
        "degrees",
        "elective_year",
        "address",
        "city",
        "neighborhood",
        "stratum",
        "phone",
        "email",
    ]


@register(models.Student)
class StudentAdmin(ModelAdmin):
    list_display = ("id", "candiate")
    search_fields = ("id", "candiate")
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "school"
