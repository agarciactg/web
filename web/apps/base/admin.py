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
