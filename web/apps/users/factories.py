import factory

from web.apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: f"Name{n}")
    last_name = factory.Sequence(lambda n: f"LastName{n}")
    email = factory.Sequence(lambda n: f"email{n}@mail.com")
    type_user = User.UserType.CUSTOMER

    class Meta:
        model = User
        django_get_or_create = ["username"]

    @factory.lazy_attribute
    def username(self):
        return factory.Faker("bothify", text="#########").evaluate(None, None, {"locale": None})

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "12345")
        obj = super()._create(model_class, *args, **kwargs)
        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        return obj
