from django.core.mail import EmailMessage
from django.db import models

from web.apps.base import managers
from web.apps.users import models as models_user


class BaseModel(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1, "Activo"
        INACTIVE = 2, "Inactivo"

    status = models.PositiveSmallIntegerField(
        "Estado", choices=Status.choices, default=Status.ACTIVE
    )
    date_created = models.DateTimeField("Fecha Creación", auto_now_add=True)
    date_updated = models.DateTimeField("Fecha Actualizado", auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class TypeDocument(BaseModel):
    class Type(models.IntegerChoices):
        NATURAL = 1, "Natural"
        BUSINESS = 2, "Empresa"

    name = models.CharField("Nombre", max_length=340)
    initials = models.CharField("Iniciales", max_length=340, null=True, blank=True)
    type_user = models.PositiveSmallIntegerField("Tipo de Usuario", choices=Type.choices)

    objects = managers.TypeDocumentManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipo de Documentos"
        ordering = ["id"]


class Province(BaseModel):
    name = models.CharField("Nombre", max_length=340)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["id"]


class City(BaseModel):
    name = models.CharField("Nombre", max_length=340)
    province = models.ForeignKey(Province, models.PROTECT, "cities", verbose_name="Provincia")

    objects = managers.CityManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ["id"]


class EmailTemplate(models.Model):
    class EmailType(models.TextChoices):
        WELCOME_EMAIL = "WELCOME_EMAIL", "Plantilla de correo de bienvenida."
        VALIDATION_EMAIL = (
            "VALIDATION_EMAIL",
            "Plantilla de correo de confirmacion de email",
        )
        CONTRACT_AUTOPAY = (
            "CONTRACT_AUTOPAY",
            "Plantilla de correo de contrato de rental.",
        )
        RECOVERY_PASSWORD = (
            "RECOVERY_PASSWORD",
            "Plantilla de correo de recuperacion de contraseña",
        )

    id = models.CharField(
        max_length=50,
        primary_key=True,
        choices=EmailType.choices,
    )
    sengrid_id = models.CharField("Sengrid ID", max_length=340, help_text="Sengrid ID")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.get_id_display()

    class Meta:
        verbose_name = "Plantilla Email"
        verbose_name_plural = "Plantillas Email"

    def send_email(self, to, context):
        if self.active:
            email = EmailMessage(to=[to])
            email.template_id = self.sengrid_id
            email.merge_global_data = context
            email.send()


class Session(BaseModel):
    user = models.ForeignKey(models_user.User, on_delete=models.PROTECT, verbose_name="usuarios")
    time_sesion = models.TimeField(verbose_name="tiempo en sesion")

    def __str__(self):
        return f"{self.time_sesion} - {self.user.username}"

    class Meta:
        verbose_name = "Sesion"
        verbose_name_plural = "Sesiones"
        ordering = ["id"]
