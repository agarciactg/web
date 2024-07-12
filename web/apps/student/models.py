import uuid
from web.apps.base.models import BaseModel
from django.db import models
from datetime import date

from web.apps.users.models import User


class Candidate(BaseModel):
    class Gender(models.IntegerChoices):
        M = 0, "Masculino"
        F = 1, "Femenino"
        OTHER = 2, "Otro"

    class Laterality(models.IntegerChoices):
        L = 0, "Izquierdo"
        R = 1, "Diestro"
        A = 2, "Ambidiestro"

    class Degrees(models.IntegerChoices):
        FIRST = 1, "Primero"
        SECOND = 2, "Segundo"
        THIRD = 3, "Tercero"
        FOURTH = 4, "Cuarto"
        FIFTH = 5, "Quinto"
        SIXTH = 6, "Sexto"
        SEVENTH = 7, "Septimo"
        EIGHTH = 8, "Octavo"
        NINTH = 9, "Noveno"
        TENTH = 10, "Decimo"
        ELEVENTH = 11, "Once"

    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, verbose_name="usuario", related_name="candidate_user"
    )
    place_of_bird = models.CharField(verbose_name="Lugar de nacimiento", max_length=350)
    date_of_bird = models.DateField(verbose_name="Fecha de nacimiento")
    years = models.IntegerField(verbose_name="edad")
    gender = models.PositiveBigIntegerField(
        verbose_name="Genero",
        choices=Gender.choices,
        null=True,
        blank=True
    )
    laterality = models.PositiveBigIntegerField(
        verbose_name="Lateralidad", choices=Laterality.choices
    )
    degrees = models.PositiveSmallIntegerField(
        verbose_name="Grado",
        help_text="Grado educativo",
        choices=Degrees.choices,
    )
    elective_year = models.IntegerField(verbose_name="Anio electivo")
    address = models.CharField(verbose_name="Direccion", max_length=350)
    city = models.CharField(verbose_name="ciudad", max_length=350)
    neighborhood = models.CharField(verbose_name="Barrio", max_length=350)
    stratum = models.IntegerField(verbose_name="Estrato")
    phone = models.CharField(verbose_name="Telefono", max_length=350, null=True, blank=True)
    email = models.CharField(verbose_name="Correo", max_length=350)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"
        ordering = ["-id"]

    @property
    def only_year(self):
        return self.elective_year.strftime('%Y')

    @property
    def age(self):
        today = date.today()
        born = self.date_of_bird
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class Student(BaseModel):
    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    candiate = models.ForeignKey(Candidate, on_delete=models.PROTECT, verbose_name="Candidato")

    def __str__(self):
        return f"{self.candiate.user.first_name} {self.candiate.user.last_name}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["-id"]
