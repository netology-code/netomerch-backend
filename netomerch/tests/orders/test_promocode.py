import pytest
from django.core.cache import cache
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from tests.baker_recipes import code, emails, item_name


@pytest.mark.django_db
class TestPromoBaker:
    """Let's test API of item's categories"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = '/api/v1/promo/'

        self.api_client = APIClient()

    def test_promo(self, promo_factory, mock_get_colors, mock_cache):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 2
        promo_factory(_quantity=quantity)

        data = {
            "code": code[0],
            "email": emails[0]
        }

        response = self.api_client.post(self.url_list, data=data, format='json')

        assert response.status_code == HTTP_200_OK
        assert response.data['item']['name'] == item_name[0]

    def test_promo_with_invalid_promo(self, promo_factory, mock_get_colors, mock_cache):

        quantity = 4

        promo_factory(_quantity=quantity)

        data = {
            "code": code[1],
            "email": emails[1]
        }

        response = self.api_client.post(self.url_list, data=data, format='json')

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data[0] == 'Incorrect code or email'

    def test_promo_with_invalid_email(self, promo_factory, mock_get_colors, mock_cache):
        quantity = 4

        promo_factory(_quantity=quantity)

        data = {
            "code": code[0],
            "email": emails[1]
        }

        response = self.api_client.post(self.url_list, data=data, format='json')

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data[0] == 'Incorrect code or email'

    def teardown(self):
        cache.clear()
