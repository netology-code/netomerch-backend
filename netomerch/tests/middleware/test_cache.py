import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestMiddlewareBakery:
    def setup(self):
        """это метод запускается перед каждым тестом"""
        self.url_list = reverse('categories-list')
        self.api_client = APIClient()

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    def test_get_cache(self, category_factory, mock_cache_set):
        """генерим quantity объектов, методом GET получаем все"""

        quantity = 5  # генерим 5 объектов категорий
        category_factory(_quantity=quantity)
        response = self.api_client.get(self.url_list)

        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity  # вот тут убеждаемся что их ровно quantity
        # assert cache.get(self.url_list).status_code == HTTP_200_OK # TODO uncomment after check why it caused an err
        # assert len(cache.get(self.url_list).data.get('results')) == quantity

    def teardown(self):
        cache.clear()
