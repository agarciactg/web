import factory

from web.apps.base.models import City, Province, TypeDocument


class TypeDocumentFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Type Document {n}")

    class Meta:
        model = TypeDocument


class ProvinceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Province


class CityFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"City {n}")
    province = factory.SubFactory(ProvinceFactory)

    class Meta:
        model = City
