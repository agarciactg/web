from rest_framework.generics import ListAPIView

from web.apps.base.api.serializers import CitySerializer, TypeDocumentSerializer
from web.apps.base.models import City, TypeDocument
from web.apps.base.utils import StandardResultsPagination
from web.utils.mixins import APIBasePermissionsMixin


# Api of  City
class CityAPIView(APIBasePermissionsMixin, ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.activos()
    pagination_class = StandardResultsPagination


# Api of  Type Documents
class TypeDocumentAPIView(APIBasePermissionsMixin, ListAPIView):
    serializer_class = TypeDocumentSerializer
    queryset = TypeDocument.objects.activos()
    pagination_class = StandardResultsPagination
