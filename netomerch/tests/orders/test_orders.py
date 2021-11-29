import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient

from apps.orders.models import ItemConnections, Order
from apps.products.models import Item


@pytest.mark.django_db
class TestOrdersBaker:
    """Let's test API of item's categories"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = reverse('orders-list')

        self.data = {
            "name": "Коля",
            "email": "xex103@yandex.ru",
            "phone": "+79295918110",
            "total_sum": 1000,
            "final_sum": 800,
            "address": "Москва, центр",
            "comment": "Тут много текста. Типо коммент"
        }

        self.api_client = APIClient()
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_create_order(self, item_factory, mock_cache, mock_sendmail):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 5
        item_factory(_quantity=quantity)

        pk = Item.objects.first()

        item = {"item": [{"items": pk.id, "count": 2}]}
        data = {**self.data, **item}

        response = self.api_client.post('/api/v1/orders/', data=data, format='json')

        pk = response.data.get('id')
        order = Order.objects.get(pk=pk)

        connect = ItemConnections.objects.filter(orders=pk).values()

        assert response.status_code == HTTP_201_CREATED
        assert order.name == self.data['name']
        assert order.comment == self.data['comment']
        assert order.discount == self.data['total_sum'] - self.data['final_sum']
        assert connect[0]['count'] == 2

    def teardown(self):
        cache.clear()
