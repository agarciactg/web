from django.conf import settings
from django.contrib.admin import ModelAdmin, register

from web.apps.base import models


@register(models.TypeDocument)
class TypeDocumentAdmin(ModelAdmin):
    list_display = (
        "name",
        "initials",
        "type_user",
    )
    search_fields = (
        "name",
        "initials",
    )
    ordering = ("-id",)
    list_filter = ("type_user", "initials")
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "description"


@register(models.EmailTemplate)
class EmailTemplateAdmin(ModelAdmin):
    list_display = ("id", "sengrid_id", "active")
    icon_name = "email"
    list_per_page = settings.NUMBER_PAGINATION_ADMIN


@register(models.Province)
class ProvinceAdmin(ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    icon_name = "location_city"
    list_per_page = settings.NUMBER_PAGINATION_ADMIN


@register(models.City)
class CityAdmin(ModelAdmin):
    list_display = ("id", "name", "province")
    search_fields = ("name", "province__name")
    icon_name = "business"
    ordering = ("name",)
    raw_id_fields = ("province",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
