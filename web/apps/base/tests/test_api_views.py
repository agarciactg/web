import json

from django.urls import resolve

from web.apps.base.api.serializers import CitySerializer
from web.apps.base.api.views import CityAPIView, TypeDocumentAPIView
from web.apps.base.tests.base_helpers import BaseAPITestCase
from web.apps.base.tests.factories import CityFactory


class BaseAPIViewsTests(BaseAPITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_cityapiview_resolves_correctly(self):
        found = resolve(self.reverse("base_api:cities"))
        self.assertTrue(found.func.__name__, CityAPIView.__name__)

    def test_cityapiview_status_200(self):
        response = self.get(self.reverse("base_api:cities"), extra=self.headers)
        self.assert_http_200_ok(response)

    def test_cityapiview_returns_list_of_active(self):
        cities = [CityFactory(status=1) for _ in range(5)]
        # create inactive city that should not be on the response
        CityFactory(status=2)

        response = self.get(self.reverse("base_api:cities"), extra=self.headers)
        result = json.loads(response.content.decode("utf8"))
        cities_content = result.get("data")
        code_transaction = result.get("code_transaction")

        self.assertEqual(code_transaction, "OK")

        cities = CitySerializer(cities, many=True).data
        for index in range(5):
            self.assertEqual(cities_content["results"][index].get("id"), cities[index].get("id"))
            self.assertEqual(
                cities_content["results"][index].get("name"), cities[index].get("name")
            )

    def test_type_document_natural_api_view_resolves_correctly(self):
        found = resolve(self.reverse("base_api:type_documents"))
        self.assertTrue(found.func.__name__, TypeDocumentAPIView.__name__)

    def test_type_document_natural_api_view_status_200(self):
        response = self.get(self.reverse("base_api:type_documents"), extra=self.headers)
        self.assert_http_200_ok(response)
