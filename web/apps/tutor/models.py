import uuid

from django.db import models

from web.apps.base.models import BaseModel
from web.apps.student.models import Candidate
from web.apps.users.models import User


class Tutor(BaseModel):
    class TypeOfHousing(models.IntegerChoices):
        own = 0, "Propia"
        rented = 1, "Arrendada"
        other = 2, "Otra"

    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, verbose_name="Usuario", related_name="tutor_user"
    )
    phone = models.CharField(max_length=350, verbose_name="Celular", blank=True, null=True)
    profession = models.CharField(max_length=350, verbose_name="Profesion", blank=True, null=True)
    email = models.CharField(max_length=350, verbose_name="Correo", blank=True, null=True)
    workplace = models.CharField(
        max_length=350, verbose_name="Lugar de trabajo", blank=True, null=True
    )
    phone_number_work = models.CharField(
        max_length=350, verbose_name="Telefono de trabajo", blank=True, null=True
    )
    monthly_income = models.CharField(
        max_length=350, verbose_name="Ingresos Mensuales", blank=True, null=True
    )
    type_of_housing = models.PositiveSmallIntegerField(
        verbose_name="Tipo de Usuario", choices=TypeOfHousing.choices, null=True, blank=True
    )
    vehicle = models.BooleanField("Tiene vehiculo?", default=False, blank=True, null=True)
    it_financial = models.BooleanField("Es acudiente financiero?", default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Acudiente"
        verbose_name_plural = "Acudientes"
        ordering = ["-id"]


class Inscription(BaseModel):
    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT, verbose_name="Candidato")
    tutors = models.ManyToManyField(
        Tutor,
        related_name="inscription_tutor",
        verbose_name="Tutor/es",
        blank=True,
        null=True
    )
    civil_registration = models.FileField(
        upload_to="civil_registration/", null=True, blank=True, verbose_name="Registro civil"
    )
    vaccination_card = models.FileField(
        upload_to="vaccination_card/", verbose_name="Carnet vacunas"
    )
    identity_card = models.FileField(
        upload_to="identity_card", verbose_name="Tarjeta identidad"
    )
    last_newsletter = models.FileField(
        upload_to="last_newsletter/", verbose_name="Ultimo boletin"
    )
    work_record = models.FileField(
        upload_to="work_record", verbose_name="Constancia laboral Acudiente"
    )
    photo_license = models.ImageField(
        upload_to="images/", null=True, blank=True, verbose_name="Foto perfil"
    )
    registration_receipt = models.ImageField(
        upload_to="registration_receipt/", verbose_name="Recibo pago de inscripcion"
    )

    def __str__(self):
        return f"{self.candidate.user.first_name}"

    class Meta:
        verbose_name = "Inscripcion"
        verbose_name_plural = "Inscripciones"
        ordering = ["-id"]
