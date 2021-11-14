import pytest

from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from django.core.cache import cache


from apps.products.models import Category

@pytest.mark.django_db
class TestMiddlewareBakery:
    def setup(self):
        """это метод запускается перед каждым тестом"""
        self.url_list = reverse('categories-list')  # перед каждым тестом - убедиться в том, что изначально объектов там 0
        self.api_client = APIClient()

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    def test_get_all_from_db(self, category_factory):
        """генерим quantity объектов, методом GET получаем все"""
        # def mock_load(self, path):
        #     return False
        cache.clear()
        # mocker.patch('apps.products.middleware.CacheMethodsMiddleware.check_path', mock_load)  # Пришлось сделать так, ибо хз, как чистить locmem
        quantity = 5  # генерим 5 объектов категорий
        category_factory(_quantity=quantity)
        response = self.api_client.get(self.url_list)

        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity  # вот тут убеждаемся что их ровно quantity

        # global data
        # data = response  # Сохраняем ответ для mock

    def test_get_all_from_cache(self):
        """Генерим мок для вызова кеша на основе предыдущего теста, проверяем, что все отработало окей"""
        # def mock_load(self, path, request):
        #     return data

        quantity = 5
        # mocker.patch('apps.products.middleware.CacheMethodsMiddleware.set_cache', mock_load)
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity
        cache.clear()

    def retrieve(self):
        Category.objects.all().delete()
