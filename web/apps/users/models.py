import re
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from web.apps.users.files import user_avatar_image_path
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


class UserManager(DjangoUserManager):
    def create_user(self, username, type_user, first_name, last_name, email="", password=None):
        # if int(type_user) == User.EMPLOYEE:
        #     if not username or not username.isdigit():
        #         raise ValueError("Users must have an number document")

        return super().create_user(
            username,
            email,
            password,
            type_user=type_user,
            first_name=first_name,
            last_name=last_name,
        )

    def create_superuser(self, username, type_user, first_name, last_name, email="", password=None):
        username = self.normalize_email(username)
        match = re.match(
            "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",  # noqa
            username,  # noqa
        )  # noqa
        if not username or not match:
            raise ValueError("Users must have a email")

        if email == "":
            email = username

        return super().create_superuser(
            username,
            email,
            password,
            type_user=0,
            first_name=first_name,
            last_name=last_name,
        )


class User(AbstractUser):
    class UserType(models.IntegerChoices):
        ADMIN = 0, "Administrador"
        RECTOR = 1, "Rector"
        DIRECTOR = 2, "Director"
        SYSTEM_CHIEF = 3, "Jefe de sistemas"
        TEACHER = 4, "Docente"
        STUDENT = 5, "Estudiante"
        TUTOR = 6, "Acudiente"
        INSTITUTION_STAFF = 7, "Otro"
        COORDINATOR = 8, "Coordinador"

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    type_user = models.PositiveSmallIntegerField(
        verbose_name="Tipo de Usuario",
        help_text="Administración / Cliente",
        choices=UserType.choices,
    )
    username = models.CharField(
        max_length=340,
        verbose_name="Username",
        unique=True,
        help_text="Numero de cedula para Cliente",
    )
    avatar = ProcessedImageField(
        verbose_name="Foto de Perfil",
        upload_to=user_avatar_image_path,
        processors=[ResizeToFill(256, 256)],
        format="JPEG",
        options={"quality": 70},
        blank=True,
        null=True,
    )
    avatar_url = models.URLField(
        max_length=250, verbose_name="Url foto de perfil", blank=True, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "type_user"]

    # @property
    # def current_institution(self):
    #     """
    #     :return Staff
    #     :rtype: StaffInstitutions
    #     """
    #     try:
    #         institution = (
    #             self.user_staff.select_related("institution")
    #             .filter(status=BaseModel.Status.ACTIVE)
    #             .latest("date_created")
    #         )
    #         return institution
    #     except ObjectDoesNotExist:
    #         return None
