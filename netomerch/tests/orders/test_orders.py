from datetime import datetime

import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient

from apps.orders.models import Order
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

    def test_create_order(self, item_factory, mock_cache):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""
        quantity = 5
        item_factory(_quantity=quantity)

        pk = Item.objects.first()

        item = {"item": [{"items": pk.id, "count": 2}]}
        data = {**self.data, **item}

        response = self.api_client.post('/api/v1/orders/', data=data, format='json')

        pk = response.data.get('id')
        order = Order.objects.get(pk=pk)
        date = str(order.create_date).split()[0]

        assert response.status_code == HTTP_200_OK
        assert order.name == self.data['name']
        assert order.comment == self.data['comment']
        assert order.discount == self.data['total_sum'] - self.data['final_sum']
        assert date == str(datetime.now().date())

    def teardown(self):
        cache.clear()
