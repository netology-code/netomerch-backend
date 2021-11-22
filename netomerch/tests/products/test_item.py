import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from apps.products.models import Category, Item, ItemProperty
from tests.products.test_category import TestCategoryBaker
from tests.products.test_itemproperty import TestItemPropertyBaker


@pytest.mark.django_db
class TestItemBaker:
    """Let's test Item's API"""

    @staticmethod
    def create_instances():
        """This method provides the ability to reuse code"""
        TestCategoryBaker.create_instances()
        TestItemPropertyBaker.create_instances()

        cat_wear = Category.objects.filter(name='wear').all()
        cat_office = Category.objects.filter(name='office').all()
        cat_startup = Category.objects.filter(name='startup').all()
        cat_present = Category.objects.filter(name='present').all()
        p_size = ItemProperty.objects.filter(name='size').all()
        p_color = ItemProperty.objects.filter(name='color').all()
        p_has_print = ItemProperty.objects.filter(name='has_print').all()
        p_print = ItemProperty.objects.filter(name='print').all()
        p_material = ItemProperty.objects.filter(name='material').all()

        i_futb = Item.objects.create(
            name='футболка',
            price=400.00,
            is_published=True,
            tags=['хит', 'хлопок'],
            properties={
                p_size.values("name").get()['name']: ['S', 'M', 'L', 'XL', 'Oversize'],
                p_material.values("name").get()['name']: ['cotton 100%'],
                p_color.values("name").get()['name']: ['black', 'white', 'yellow'],
                p_has_print.values("name").get()['name']: ['1']
            }
        )
        i_futb.category.add(cat_wear.get(), cat_startup.get())

        i_notebook = Item.objects.create(
            name='блокнот',
            price=50.00,
            is_published=True,
            tags=['хит', 'старт'],
            properties={
                p_size.values("name").get()['name']: ['A5'],
                p_color.values("name").get()['name']: ['black', 'blue'],
            }
        )
        i_notebook.category.add(cat_office.get(), cat_startup.get(), cat_present.get())

        i_cup_print = Item.objects.create(
            name='чашка с принтом',
            price=150.00,
            is_published=True,
            tags=['хит', 'подарок', 'принт'],
            properties={
                p_material.values("name").get()['name']: ['ceramics'],
                p_color.values("name").get()['name']: ['white'],
                p_has_print.values("name").get()['name']: [True],
                p_print.values("name").get()['name']: ['Happy New Year', 'Marry Christmas', 'Mother’s Day'],
            }
        )
        i_cup_print.category.add(cat_office.get(), cat_present.get())

        i_cup_it = Item.objects.create(
            name='чашка айтишника',
            price=150.00,
            is_published=True,
            tags=['хит', 'подарок'],
            properties={
                p_material.values("name").get()['name']: ['ceramics'],
                p_color.values("name").get()['name']: ['blue', 'white'],
                p_has_print.values("name").get()['name']: [False],
            }
        )
        i_cup_it.category.add(cat_office.get(), cat_present.get())

        i_cup_project = Item.objects.create(
            name='чашка ПМ',
            price=150.00,
            is_published=True,
            tags=['хит', 'подарок'],
            properties={
                p_material.values("name").get()['name']: ['ceramics'],
                p_color.values("name").get()['name']: ['blue', 'white'],
                p_has_print.values("name").get()['name']: [False],
            }
        )
        i_cup_project.category.add(cat_office.get(), cat_present.get())

        i_cup_analyst = Item.objects.create(
            name='чашка Аналитика',
            price=150.00,
            is_published=False,
            tags=['хит', 'подарок'],
            properties={
                p_material.values("name").get()['name']: ['ceramics'],
                p_color.values("name").get()['name']: ['blue', 'white', 'black'],
                p_has_print.values("name").get()['name']: [False],
            }
        )
        i_cup_analyst.category.add(cat_office.get(), cat_present.get())

        i_cup_strange = Item.objects.create(
            name='чашка Стрейнджерса',
            price=150.00,
            is_published=True,
            tags=['хит', 'подарок'],
            properties={
                p_material.values("name").get()['name']: ['ceramics'],
                p_color.values("name").get()['name']: ['blue', 'white', 'black'],
                p_has_print.values("name").get()['name']: [False],
            }
        )
        i_cup_strange.category.add(cat_office.get(), cat_present.get())

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = reverse('items-list')
        print(self.url_list)
        self.items_count = 0

        # Do we have an empty database?
        self.api_client = APIClient()
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0
        self.create_instances()

    def test_get_all_by_anonymous_user(self, test_password, create_admin, create_customer, mock_cache):
        """We take all objects with the GET method
        except 1 with is_published=False property"""

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)
        items_count = Item.objects.all().filter(is_published=True).count()
        self.api_client.logout

        customer = create_customer()
        self.api_client.login(username=customer.username, password=test_password)

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == items_count

        self.api_client.logout

    def test_get_all_by_admin(self, test_password, create_admin, mock_cache):
        """We take all objects with the GET method,
        includind items with is_published=False property"""

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)
        items_count = Item.objects.all().count()

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == items_count

        self.api_client.logout()

    def test_get_first(self, mock_cache):
        """It generates the "quantity" of objects, then we take the first one with the GET method"""

        item_1 = Item.objects.first()
        url = reverse('items-detail', kwargs={'pk': item_1.pk})
        response = self.api_client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('name') == item_1.name

    def test_delete_by_not_admin(self, mock_cache):
        """We can't delete the item because we are not admin user"""

        item_del = Item.objects.first()
        url = reverse('items-detail', kwargs={'pk': item_del.pk})

        response_del = self.api_client.delete(url)
        assert response_del.status_code == HTTP_403_FORBIDDEN

    def test_delete_by_admin(self, test_password, create_admin, mock_cache):
        """We can delete the item because we are admin now"""

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)
        item_del = Item.objects.first()
        url_del = reverse('items-detail', kwargs={'pk': item_del.pk})
        print(f"url_del: {url_del}")
        items_count = Item.objects.all().count()

        response_del = self.api_client.delete(url_del)
        assert response_del.status_code == HTTP_204_NO_CONTENT

        response_after_del = self.api_client.get(self.url_list)
        assert response_after_del.status_code == HTTP_200_OK
        print(response_after_del.data)
        assert len(response_after_del.data.get('results')) == items_count - 1

    def test_delete_by_admin_fail_id(self, test_password, create_admin, mock_cache):
        """We can't delete the failed id's item even we are admin """

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        pk = -100500
        url = reverse('items-detail', kwargs={'pk': pk})
        response_del = self.api_client.delete(url)
        assert response_del.status_code == HTTP_404_NOT_FOUND

        self.api_client.logout()

    def test_without_ordering(self, mock_cache):
        """We take all objects with the GET method
        In this test we use the "ordering" clause with ordering by pk (created)"""

        response = self.api_client.get(self.url_list, data={'ordering': 'id'})
        first = response.data.get('results')[0]
        last = response.data.get('results')[-1]

        assert response.status_code == HTTP_200_OK
        # here we make sure that the first's object name is the first's created name,
        #  and that the last's object name is the last's created name
        assert first.get('name') == 'футболка'
        assert last.get('name') == 'чашка Стрейнджерса'

    def test_with_ordering(self, mock_cache):
        """We take all objects with the GET method
        In this test we use the "ordering" clause (field 'name')"""

        response = self.api_client.get(self.url_list, data={'ordering': 'name'})
        first = response.data.get('results')[0]
        last = response.data.get('results')[-1]

        assert response.status_code == HTTP_200_OK
        # here we make sure that the first's object name is the first's one sorted by field 'name',
        #  and that the last's object name is the last's one sorted by field 'name'
        assert first.get('name') == 'блокнот'
        assert last.get('name') == 'чашка с принтом'

    def test_count_2_objects_by_search_admin(self, create_admin, test_password, mock_cache):
        """We make sure that using search string 'Ика' we can find only 2 objects,
        because we are admin now"""

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'search': 'Ика'})
        assert response.status_code == HTTP_200_OK
        print(response.data.get('results'))
        assert len(response.data.get('results')) == 2

        self.api_client.logout()

    def test_count_1_object_by_search_customer(self, create_customer, test_password, mock_cache):
        """We make sure that using search string 'Ика' we can find only 2 objects,
        because we are customer now"""

        customer = create_customer()
        self.api_client.login(username=customer.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'search': 'Ика'})
        assert response.status_code == HTTP_200_OK
        print(response.data.get('results'))
        assert len(response.data.get('results')) == 1

        self.api_client.logout()

    def test_count_0_objects_by_search_admin(self, create_admin, test_password, mock_cache):
        """We make sure that we can't find any objects with the search string 'test' """

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'search': 'test'})
        assert response.status_code == HTTP_200_OK
        print(response.data.get('results'))
        assert len(response.data.get('results')) == 0

        self.api_client.logout()

    def test_filter_by_correct_category_office_admin(self, create_admin, test_password, mock_cache):
        """We make sure that we find all items, including is_published=False property"""

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'category__name': 'office'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 6

        self.api_client.logout()

    def test_filter_by_correct_category_office_customer(self, create_customer, test_password, mock_cache):
        """We make sure that we find all items, excluding is_published=False property"""

        customer = create_customer()
        self.api_client.login(username=customer.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'category__name': 'office'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 5

        self.api_client.logout()

    def test_filter_by_incorrect_category_oddice_admin(self, create_admin, test_password, mock_cache):
        """We make sure that we can't find any items even we are admin now"""

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'category__name': 'oddice'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

        self.api_client.logout()

    def teardown(self):

        cache.clear()
