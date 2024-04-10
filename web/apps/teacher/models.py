import uuid
from web.apps.base.models import BaseModel
from django.db import models
from web.apps.users import models as models_user


class Teacher(BaseModel):
    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(
        models_user.User, on_delete=models.PROTECT, verbose_name="usuario", related_name="teacher"
    )
    profession = models.CharField("Profecion", max_length=340, db_index=True)
    is_full_time = models.BooleanField("Es tiempo completo", default=False)

    def __str__(self):
        return f"{self.user.username} - {self.profession}"

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ["id"]


class Subject(BaseModel):
    uuid = models.UUIDField("UUID", unique=True, default=uuid.uuid4, editable=False, db_index=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name="Profesor")
    name = models.CharField("Nombre", max_length=340)
    description = models.TextField("Descripcion", blank=True, null=True)
    credis = models.IntegerField("Creditos", default=0, null=True, blank=True)
    hours = models.TimeField("Horas", default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.user.username}"

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = ["id"]
