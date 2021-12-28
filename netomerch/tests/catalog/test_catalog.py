import pytest
from django.core.cache import cache
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from tests.baker_recipes import category_name, item_name, size_name, spec_name


@pytest.mark.django_db
class TestOrdersBaker:
    """Let's test API of item's categories"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = '/api/v1/catalog/'

        self.api_client = APIClient()
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data['categories']) == 0

    def test_catalog(self, item_factory, category_factory, specialization_factory, mock_cache, mock_sendmail):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 4
        item_factory(_quantity=quantity)
        category_factory(_quantity=quantity)
        specialization_factory(_quantity=quantity)

        response = self.api_client.get(self.url_list)

        assert response.status_code == HTTP_200_OK
        assert len(response.data['categories']) > 0
        assert len(response.data['specialization']) > 0
        assert len(response.data['sizes']) > 0
        assert len(response.data['items']) == quantity - 1
        assert response.data['items'][0]['name'] == item_name[0]
        assert response.data['categories'][0]['name'] in category_name
        assert response.data['specialization'][0]['name'] in spec_name
        assert response.data['sizes'][0]['name'] in size_name

    def teardown(self):
        cache.clear()
