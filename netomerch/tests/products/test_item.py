# import pytest
# from django.core.cache import cache
# from django.urls import reverse
# from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
# from rest_framework.test import APIClient

# from apps.products.models import Category, Item


# @pytest.mark.django_db
# class TestItemBaker:
#     """тестируем АПИ товаров (продуктов)"""

#     def setup(self):
#         """этот метод вызывается перед каждым тестом"""
#         self.url_list = reverse('items-list')

#         # перед каждым тестом - убедиться в том, что изначально объектов там 0, а потом создаём объекты
#         self.api_client = APIClient()
#         response = self.api_client.get(self.url_list)
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 0
#         self.create_instances()

#     @staticmethod
#     def create_instances():
#         """чтобы не повторять этот код несколько раз, создаём 2 категории и 5 продуктов"""
#         Category.objects.bulk_create(
#             [
#                 Category(category_name='Футболки', short_description='футб'),
#                 Category(category_name='Носки', short_description='носк'),
#             ]
#         )
#         c1 = Category.objects.filter(category_name='Футболки').first()
#         c2 = Category.objects.filter(category_name='Носки').first()

#         Item.objects.bulk_create(
#             [
#                 Item(item_name='Футболка1', description='футб1', category_id=c1, is_published=True, default_price=100),
#                 Item(item_name='Футболка2', description='футб2', category_id=c1, is_published=False, default_price=150),
#                 Item(item_name='Носки1', description='носки1', category_id=c2, is_published=True, default_price=1020),
#                 Item(item_name='Футболка3', description='ф3', category_id=c1, is_published=True, default_price=1230),
#                 Item(item_name='Носки2', description='нос2', category_id=c2, is_published=True, default_price=25),
#             ]
#         )

#     def test_get_all_by_anonymous_user(self, mock_cache):
#         """создаём 5 объектов, без авторизации увидим 4, ибо 1 выключен"""

#         response = self.api_client.get(self.url_list)
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 4  # вот тут убеждаемся что их 4, ибо одна не видна

#     def test_get_all_by_admin(self, test_password, create_admin, mock_cache):
#         """создаём 5 объектов, авторизовались, увидели все 5"""

#         admin = create_admin()
#         self.api_client.login(username=admin.username, password=test_password)  # залогинились под ним

#         response = self.api_client.get(self.url_list)
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 5  # вот тут убеждаемся что их 4, ибо одна не видна

#         self.api_client.logout()

#     def test_get_first(self, mock_cache):
#         """создаём 5 объектов, методом GET получаем первый"""

#         item_1 = Item.objects.filter(pk__gt=0).first()
#         url = reverse('items-detail', kwargs={'pk': item_1.pk})
#         response = self.api_client.get(url)
#         assert response.status_code == HTTP_200_OK
#         assert response.data.get('item_name') == item_1.item_name  # вот тут убеждаемся что имена совпадают

#     def test_delete_by_not_admin(self):
#         """методом DELETE удалим первый товар, нельзя всем кроме админа"""

#         item_del = Item.objects.filter(pk__gt=0).first()  # удалим первый, например
#         url = reverse('items-detail', kwargs={'pk': item_del.pk})

#         response_del = self.api_client.delete(url)
#         assert response_del.status_code == HTTP_403_FORBIDDEN  # без логина - нельзя удалять!

#     def test_delete_by_admin(self, test_password, create_admin):
#         """методом DELETE удалим первый товар, админу можно"""

#         item_del = Item.objects.filter(pk__gt=0).first()  # удалим первый, например
#         url_del = reverse('items-detail', kwargs={'pk': item_del.pk})

#         admin = create_admin()
#         self.api_client.login(username=admin.username, password=test_password)  # залогинились под ним

#         response_del = self.api_client.delete(url_del)
#         assert response_del.status_code == HTTP_204_NO_CONTENT  # и вот тут всё ок

#         response_after_del = self.api_client.get(self.url_list)
#         assert response_after_del.status_code == HTTP_200_OK
#         assert len(response_after_del.data) == 4  # проверяем - было 5, осталось 4

#         random_pk = 100500  # допустим у нас точно нет такого первичного ключа
#         url = reverse('items-detail', kwargs={'pk': random_pk})
#         response_del = self.api_client.delete(url)  # пытаемся удалить несуществующий
#         assert response_del.status_code == HTTP_404_NOT_FOUND  # нельзя удалить

#         self.api_client.logout()

#     def test_without_ordering(self, mock_cache):
#         """создаём 5 объектов, берём первый и последний, не указываем ordering, 1 не видим"""

#         response = self.api_client.get(self.url_list)  # ещё не применяем ordering
#         product_first = response.data.get('results')[0]  # первый объект
#         product_last = response.data.get('results')[3]  # последний объект

#         assert response.status_code == HTTP_200_OK
#         assert product_first.get('item_name') == 'Футболка1'
#         assert product_last.get('item_name') == 'Носки2'  # объекты идут в том порядке, в котором мы их создали

#     def test_with_ordering(self, mock_cache):
#         """создаём 5 объектов, берём первый и последний, проверяем сортировку по имени, 1 не видим"""

#         response = self.api_client.get(self.url_list, data={'ordering': 'item_name'})  # сортируем по имени
#         product_first = response.data.get('results')[0]  # первый объект
#         product_last = response.data.get('results')[3]  # последний объект

#         assert response.status_code == HTTP_200_OK
#         assert product_first.get('item_name') == 'Носки1'
#         assert product_last.get('item_name') == 'Футболка3'  # и вот теперь сортировка сработала (по алфавиту)

#     def test_search_by_name_ok_1(self, mock_cache):
#         """создаём 5 объектов, ищем какие-то в них"""

#         response = self.api_client.get(self.url_list, data={'search': 'фуТбоЛКа'})  # регистронезависимо
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 2  # найдём 2 футболки, ибо 1 не видна

#     def test_search_by_name_ok_2(self, test_password, create_admin, mock_cache):
#         """создаём 5 объектов, ищем какие-то в них"""

#         admin = create_admin()
#         self.api_client.login(username=admin.username, password=test_password)  # залогинились под ним

#         response = self.api_client.get(self.url_list, data={'search': 'фуТбоЛКа'})  # регистронезависимо
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 3  # а вот админ найдёт все 3

#         self.api_client.logout()

#     def test_search_by_name_ok_3(self, mock_cache):
#         """создаём 5 объектов, ищем какие-то в них"""

#         response = self.api_client.get(self.url_list, data={'search': 'нос'})
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 2  # найдём двое носков

#     def test_search_by_name_not_ok(self, mock_cache):
#         """создаём 5 объектов, ищем какие-то в них, теперь те, которых там нет"""

#         response = self.api_client.get(self.url_list, data={'search': 'Майка'})
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 0  # а майки не найдём, ведь их нет

#     def test_search_by_non_search_field(self, mock_cache):
#         """создаём 5 объектов, ищем какие-то в них по полю, по которому нельзя искать, например description"""

#         response = self.api_client.get(self.url_list, data={'search': 'ф3'})  # в description оно есть, но не найдётся

#         # по полю description искать нельзя, но если его добавить в search_fields, тогда тут будет уже 5!
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 0

#     def test_filter_by_correct_category_1(self, mock_cache):
#         """фильтруем продукты по категориям, по правильным"""

#         response = self.api_client.get(self.url_list, data={'category_id__category_name': 'Футболки'})
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 2  # найдём 2 футболки, ибо 1 не видна

#     def test_filter_by_correct_category_2(self, mock_cache):
#         """фильтруем продукты по категориям, по правильным"""

#         response = self.api_client.get(self.url_list, data={'category_id__category_name': 'Носки'})
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 2  # найдём 2 носков

#     def test_filter_by_wrong_field(self, mock_cache):
#         """фильтруем продукты по неправильному полю, неправильный фильтр, вернутся все товары, фильтр не сработает"""

#         response = self.api_client.get(self.url_list, data={'name': 'Категория которой нет'})
#         assert response.status_code == HTTP_200_OK  # все ещё HTTP_200_OK, но
#         assert len(response.data.get('results')) == 4  # нашли все видимые, ибо такой фильтр не работает

#     def test_str_model(self, mock_cache):
#         """проверям что модель распечатается как указано в методе __str__"""

#         item_1 = Item.objects.first()
#         assert str(item_1) == f'{item_1.id}: Category {item_1.category_id}, name {item_1.item_name}'

#     def teardown(self):
#         cache.clear()
