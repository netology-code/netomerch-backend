import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from apps.products.models import Category


@pytest.mark.django_db
class TestCategoryBaker:
    """тестируем АПИ категорий"""
    def setup(self):
        """это метод запускается перед каждым тестом"""
        self.url_list = reverse('categories-list')
        # перед каждым тестом - убедиться в том, что изначально объектов там 0
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

    def test_get_all(self, category_factory, mock_cache):
        """генерим quantity объектов, методом GET получаем все"""
        quantity = 5  # генерим 5 объектов категорий
        category_factory(_quantity=quantity)
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity  # вот тут убеждаемся что их ровно quantity

    def test_get_first(self, category_factory, mock_cache):
        """генерим quantity объектов, методом GET получаем первый"""
        quantity = 5
        category_factory(_quantity=quantity)
        c_1 = Category.objects.filter(pk__gt=0).first()  # TODO: и здесь тоже этот же костыль
        url = reverse('categories-detail', kwargs={'pk': c_1.pk})
        response = self.api_client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('category_name') == c_1.category_name  # вот тут убеждаемся что имена совпадают

    def test_without_ordering(self, mock_cache):
        """создаём 4 объекта, берём первый и последний, не указываем ordering"""

        self.create_instances()  # создали 4 объекта

        response = self.api_client.get(self.url_list)  # ещё не применяем ordering
        cat_first = response.data.get('results')[0]  # первый объект
        cat_last = response.data.get('results')[3]  # последний объект

        assert response.status_code == HTTP_200_OK
        assert cat_first.get('category_name') == 'Футболки'
        assert cat_last.get('category_name') == 'Футболки женские'  # объекты идут в том порядке, в котором созданы

    def test_with_ordering(self, mock_cache):
        """создаём 4 объекта, берём первый и последний, проверяем сортировку по имени"""

        self.create_instances()  # создали 5 объектов

        response = self.api_client.get(self.url_list, data={'ordering': 'category_name'})  # сортируем по имени
        cat_first = response.data.get('results')[0]  # первый объект
        cat_last = response.data.get('results')[3]  # последний объект

        assert response.status_code == HTTP_200_OK
        assert cat_first.get('category_name') == 'Блокноты'
        assert cat_last.get('category_name') == 'Чашки'  # и вот теперь сортировка сработала (по алфавиту)

    def test_search_by_name_ok_1(self, mock_cache):
        """создаём 4 объекта, ищем какие-то в них"""

        self.create_instances()  # создали 4 объекта

        response = self.api_client.get(self.url_list, data={'search': 'фУтБ'})  # регистронезависимо
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 2  # найдём две категории

    def test_search_by_name_ok_2(self, mock_cache):
        """создаём 4 объекта, ищем какие-то в них"""

        self.create_instances()  # создали 4 объекта

        response = self.api_client.get(self.url_list, data={'search': 'Чаш'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 1  # найдём одну категорию

    def test_search_by_name_not_ok(self, mock_cache):
        """создаём 4 объекта, ищем какие-то в них, теперь те, которых там нет"""

        self.create_instances()  # создали 4 объекта

        response = self.api_client.get(self.url_list, data={'search': 'а такого нет'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0  # ничё не найдём, ведь такой категории нет

    def test_search_by_non_search_field(self, mock_cache):
        """создаём 4 объекта, ищем какие-то в них по полю, по которому нельзя искать, например description"""

        self.create_instances()  # создали 4 объекта

        response = self.api_client.get(self.url_list, data={'search': 'description'})  # регистронезависимо

        # по полю description пока искать нельзя, но если его добавить в search_fields, тогда тут будет уже 4!
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    def test_str_model(self, mock_cache):
        """проверям что модель распечатается как указано в методе __str__"""

        self.create_instances()

        cat_first = Category.objects.first()
        assert str(cat_first) == f'{cat_first.id}: name {cat_first.category_name}'

    def teardown(self):
        cache.clear()
