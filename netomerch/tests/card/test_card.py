import pytest
from django.core.cache import cache
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from apps.reviews.models import Review
from tests.baker_recipes import item_name


@pytest.mark.django_db
class TestOrdersBaker:
    """Let's test API of item's categories"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = '/api/v1/card/'

        self.api_client = APIClient()
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_card(self, item_factory, order_factory, review_factory, mock_cache, mock_get_colors, mock_sendmail):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 4
        item_factory(_quantity=quantity)
        order_factory(_quantity=quantity)
        review_factory(_quantity=quantity)

        pk = Review.objects.first()

        response = self.api_client.get(f'{self.url_list}{pk.item.id}/')

        assert response.status_code == HTTP_200_OK
        assert response.data['item_id'] == pk.item.id
        assert response.data['name'] == item_name[0]

    def teardown(self):
        cache.clear()
