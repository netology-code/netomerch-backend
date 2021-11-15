import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from apps.products.models import Category


@pytest.mark.django_db
class TestMiddlewareBakery:
    def setup(self):
        """это метод запускается перед каждым тестом"""
        self.url_list = reverse('categories-list')
        self.api_client = APIClient()

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    @staticmethod
    def create_instances():
        """чтобы не повторять этот код несколько раз"""
        Category.objects.bulk_create(
            [
                Category(category_name='Футболки', short_description='футб'),
                Category(category_name='Чашки', short_description='чашки'),
                Category(category_name='Блокноты', short_description='блокноты'),
                Category(category_name='Футболки женские', short_description='хватай на лету!'),
            ]
        )

    def test_get_cache(self, category_factory):
        """генерим quantity объектов, методом GET получаем все"""

        quantity = 5  # генерим 5 объектов категорий
        category_factory(_quantity=quantity)
        response = self.api_client.get(self.url_list)

        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity  # вот тут убеждаемся что их ровно quantity
        assert cache.get(self.url_list).status_code == HTTP_200_OK
        assert len(cache.get(self.url_list).data.get('results')) == quantity

    def test_with_search_bd(self):
        self.create_instances()  # создали 4 объекта

        response = self.api_client.get(self.url_list, data={'search': 'Футб'})  # регистронезависимо
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 2
        assert cache.get(self.url_list) is None

    def teardown(self):
        cache.clear()
