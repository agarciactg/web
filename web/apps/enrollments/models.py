import uuid

from web.apps.base.models import BaseModel
from web.apps.teacher import models as models_teacher
from web.apps.users import models as models_user
from django.db import models


class AcademicGroups(BaseModel):
    class Degress(models.IntegerChoices):
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
    teachers = models.ManyToManyField(
        models_teacher.Teacher,
        related_name="academic_teachers",
        verbose_name="Profesor(es)",
        blank=True,
    )
    code = models.CharField("Codigo", max_length=340, null=True, blank=True)
    name = models.CharField("Nombre", max_length=340, null=True, blank=True)
    degress = models.PositiveSmallIntegerField(
        verbose_name="Grado",
        help_text="Grado educativo",
        choices=Degress.choices,
    )

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Grado Academico"
        verbose_name_plural = "Grados Academicos"


class Enrollment(BaseModel):
    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    academic_groups = models.ForeignKey(
        AcademicGroups, on_delete=models.PROTECT, verbose_name="Grupos Academicos"
    )
    subjects = models.ManyToManyField(
        models_teacher.Subject,
        related_name="enrollment_subjects",
        verbose_name="Asignatura(s)",
        blank=True,
    )
    student = models.ForeignKey(
        models_user.User, on_delete=models.PROTECT, verbose_name="Estudiante"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Fecha registro"
    )

    def __str__(self):
        return f"{self.student.username} - {self.academic_groups.name}"

    class Meta:
        verbose_name = "Matricula"
        verbose_name_plural = "Matriculas"
        ordering = ["id"]
