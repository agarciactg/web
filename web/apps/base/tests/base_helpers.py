from rest_framework_api_key.models import APIKey
from test_plus import APITestCase, TestCase


class BaseTestCaseMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_key, cls.key = APIKey.objects.create_key(name="SUPER_KEY")
        cls.headers = {"HTTP_X_API_KEY": cls.key, "format": "json"}


class BaseAPITestCase(BaseTestCaseMixin, APITestCase):
    pass


class BaseTestCase(BaseTestCaseMixin, TestCase):
    pass
