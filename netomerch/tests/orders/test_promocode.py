import pytest
from django.core.cache import cache
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from apps.orders.baker_recipes import code
from apps.products.baker_recipes import item_name


@pytest.mark.django_db
class TestPromoBaker:
    """Let's test API of item's categories"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = '/api/v1/promo/'

        self.api_client = APIClient()

    def test_get_promo(self, promo_factory, mock_get_colors, mock_cache):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 2
        promo_factory(_quantity=quantity)

        response = self.api_client.get(f'{self.url_list}{code[0]}/')

        assert response.status_code == HTTP_200_OK
        assert response.data.get('item').get('name') == item_name[0]

    def teardown(self):
        cache.clear()
