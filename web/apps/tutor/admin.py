from django.conf import settings
from django.contrib.admin import ModelAdmin, register
from django.utils.html import format_html
from web.apps.tutor import models


@register(models.Tutor)
class TutorAdmin(ModelAdmin):
    list_display = ("id", "user", "profession", "email", "status")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "face"
    fields = [
        "user",
        "phone",
        "profession",
        "email",
        "workplace",
        "phone_number_work",
        "monthly_income",
        "type_of_housing",
        "vehicle",
        "it_financial",
    ]


@register(models.Inscription)
class InscriptionAdmin(ModelAdmin):
    list_display = (
        "id",
        "candidate",
        "civil_registration_link",
        "vaccination_card_link",
        "identity_card_link",
        "last_newsletter_link",
        "work_record_link",
        "photo_license",
        "registration_receipt_link",
    )
    search_fields = ("id", "candidate")
    ordering = ("-id",)
    list_per_page = settings.NUMBER_PAGINATION_ADMIN
    icon_name = "note_add"
    fields = [
        "candidate",
        "tutors",
        "civil_registration",
        "vaccination_card",
        "identity_card",
        "last_newsletter",
        "work_record",
        "photo_license",
        "registration_receipt",
    ]

    def civil_registration_link(self, obj):
        if obj.civil_registration:
            return format_html('<a href="{}">{}</a>', obj.civil_registration.url, "Download")
        return "-"

    def vaccination_card_link(self, obj):
        if obj.vaccination_card:
            return format_html('<a href="{}">{}</a>', obj.vaccination_card.url, "Download")
        return "-"

    def identity_card_link(self, obj):
        if obj.identity_card:
            return format_html('<a href="{}">{}</a>', obj.identity_card.url, "Download")
        return "-"

    def last_newsletter_link(self, obj):
        if obj.last_newsletter:
            return format_html('<a href="{}">{}</a>', obj.last_newsletter.url, "Download")
        return "-"

    def work_record_link(self, obj):
        if obj.work_record:
            return format_html('<a href="{}">{}</a>', obj.work_record.url, "Download")
        return "-"

    def registration_receipt_link(self, obj):
        if obj.registration_receipt:
            return format_html('<a href="{}">{}</a>', obj.registration_receipt.url, "Download")
        return "-"
