import pytest
from django.core.cache import cache
from rest_framework.status import HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient

from apps.orders.models import ItemConnections, Order
from apps.products.models import Item
from tests.baker_recipes import code


@pytest.mark.django_db
class TestOrdersBaker:
    """Let's test API of item's categories"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = '/api/v1/orders/'

        self.data = {
            "name": "Test",
            "email": "mail@mail.ru",
            "phone": "+79999999999",
            "address": "TestAddress",
            "comment": "TestComment",
            "total_sum": 2500,
            "final_sum": 2500
        }

        self.api_client = APIClient()
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_create_order_without_promo(self, item_factory, mock_cache, mock_sendmail):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 4
        item_factory(_quantity=quantity)

        pk = Item.objects.first()
        items = {
            "items": [
                {
                    "item_id": pk.id,
                    "count": 1,
                    "size": "L",
                    "color": "Белый",
                    "price": 2500
                }
            ]
        }

        data = {**self.data, **items}

        response = self.api_client.post('/api/v1/orders/', data=data, format='json')

        pk = response.data.get('id')
        order = Order.objects.get(pk=pk)

        connect = ItemConnections.objects.filter(order=pk).values()

        assert response.status_code == HTTP_201_CREATED
        assert order.name == self.data['name']
        assert order.comment == self.data['comment']
        assert connect[0]['count'] == 1

    def test_create_with_promo(self, item_factory, promo_factory, mock_cache, mock_sendmail):
        quantity = 4
        item_factory(_quantity=quantity)
        promo_factory(_quantity=quantity)

        pk = Item.objects.first()
        add_data = {
            "code": code[0],
            "items": [
                {
                    "item_id": pk.id,
                    "count": 1,
                    "size": "L",
                    "color": "Белый",
                    "price": 2500
                }
            ]
        }

        data = {**self.data, **add_data}

        response = self.api_client.post('/api/v1/orders/', data=data, format='json')

        assert response.status_code == HTTP_201_CREATED

        pk = response.data.get('id')
        order = Order.objects.get(pk=pk)

        connect = ItemConnections.objects.filter(order=pk).values()

        assert response.status_code == HTTP_201_CREATED
        assert order.name == self.data['name']
        assert order.comment == self.data['comment']
        assert connect[0]['count'] == 1

    def teardown(self):
        cache.clear()
