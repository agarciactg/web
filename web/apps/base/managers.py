import logging

from django.db import models

logger = logging.getLogger(__name__)


class TypeDocumentManager(models.Manager):
    def activos(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def natural(self):
        return self.filter(
            status=self.model.Status.ACTIVE, type_user=self.model.TypeDocument.Type.NATURAL
        )

    def business(self):
        return self.filter(status=self.model.Status.ACTIVE, type_user=self.model.Type.BUSINESS)


class CityManager(models.Manager):
    def activos(self):
        return self.filter(status=self.model.Status.ACTIVE)
