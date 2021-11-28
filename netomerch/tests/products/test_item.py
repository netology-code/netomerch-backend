import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from apps.products.models import Item


@pytest.mark.django_db
class TestItemBaker:
    """Let's test Item's API"""

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

    def test_get_all_by_anonymous_user(self, item_factory, mock_cache):
        """We take all objects with the GET method
        except 1 with is_published=False property"""

        quantity = 7
        item_factory(_quantity=quantity)

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity - 1

    def test_get_all_by_admin(self, test_password, create_admin, item_factory, mock_cache):
        """We take all objects with the GET method,
        includind items with is_published=False property"""
        quantity = 7
        item_factory(_quantity=quantity)

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quantity

        self.api_client.logout()

    def test_get_first(self, item_factory, mock_cache):
        """It generates the "quantity" of objects, then we take the first one with the GET method"""
        quantity = 7
        item_factory(_quantity=quantity)

        pk = Item.objects.first()

        url = reverse('items-detail', kwargs={'pk': pk.id})
        response = self.api_client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('name') == 'футболка'

    def test_delete_by_not_admin(self, item_factory, mock_cache):
        """We can't delete the item because we are not admin user"""

        quantity = 7
        item_factory(_quantity=quantity)

        pk = Item.objects.first()

        url = reverse('items-detail', kwargs={'pk': pk.id})

        response_del = self.api_client.delete(url)
        assert response_del.status_code == HTTP_403_FORBIDDEN

    def test_delete_by_admin(self, test_password, create_admin, item_factory, mock_cache):
        """We can delete the item because we are admin now"""
        quantity = 7
        item_factory(_quantity=quantity)
        pk = Item.objects.first()

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)
        url_del = reverse('items-detail', kwargs={'pk': pk.id})

        response_del = self.api_client.delete(url_del)
        assert response_del.status_code == HTTP_204_NO_CONTENT

        response_after_del = self.api_client.get(self.url_list)
        assert response_after_del.status_code == HTTP_200_OK
        assert len(response_after_del.data.get('results')) == quantity - 1
        self.api_client.logout()

    def test_delete_by_admin_fail_id(self, test_password, create_admin, item_factory, mock_cache):
        """We can't delete the failed id's item even we are admin """

        quantity = 7
        item_factory(_quantity=quantity)

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        pk = -100500
        url = reverse('items-detail', kwargs={'pk': pk})
        response_del = self.api_client.delete(url)
        assert response_del.status_code == HTTP_404_NOT_FOUND

        self.api_client.logout()

    def test_without_ordering(self, item_factory, mock_cache):
        """We take all objects with the GET method
        In this test we use the "ordering" clause with ordering by pk (created)"""

        quantity = 7
        item_factory(_quantity=quantity)

        response = self.api_client.get(self.url_list, data={'ordering': 'id'})
        first = response.data.get('results')[0]
        last = response.data.get('results')[-1]

        assert response.status_code == HTTP_200_OK
        assert first.get('name') == 'футболка'
        assert last.get('name') == 'чашка Стрейнджерса'

    def test_with_ordering(self, item_factory, mock_cache):
        """We take all objects with the GET method
        In this test we use the "ordering" clause (field 'name')"""
        quantity = 7
        item_factory(_quantity=quantity)

        response = self.api_client.get(self.url_list, data={'ordering': 'name'})
        first = response.data.get('results')[0]
        last = response.data.get('results')[-1]

        assert response.status_code == HTTP_200_OK
        assert first.get('name') == 'блокнот'
        assert last.get('name') == 'чашка с принтом'

    def test_count_2_objects_by_search_admin(self, create_admin, test_password, item_factory, mock_cache):
        """We make sure that using search string 'Ика' we can find only 2 objects,
        because we are admin now"""
        quantity = 7
        item_factory(_quantity=quantity)

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'search': 'Ика'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 2

        self.api_client.logout()

    def test_count_1_object_by_search_customer(self, item_factory, mock_cache):
        """We make sure that using search string 'Ика' we can find only 2 objects,
        because we are customer now"""
        quantity = 7
        item_factory(_quantity=quantity)

        response = self.api_client.get(self.url_list, data={'search': 'Ика'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 1

    def test_count_0_objects_by_search_admin(self, create_admin, test_password, item_factory, mock_cache):
        """We make sure that we can't find any objects with the search string 'test' """
        quantity = 7
        item_factory(_quantity=quantity)

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'search': 'test'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

        self.api_client.logout()

    def test_filter_by_correct_category_office_admin(self, create_admin, test_password, item_factory, mock_cache):
        """We make sure that we find all items, including is_published=False property"""
        quantity = 7
        item_factory(_quantity=quantity)

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        quant = Item.objects.filter(category__name='office').count()

        response = self.api_client.get(self.url_list, data={'category__name': 'office'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quant

        self.api_client.logout()

    def test_filter_by_correct_category_office_customer(self, item_factory, mock_cache):
        """We make sure that we find all items, excluding is_published=False property"""
        quantity = 7
        item_factory(_quantity=quantity)

        quant = Item.objects.filter(category__name='office').filter(is_published=True).count()

        response = self.api_client.get(self.url_list, data={'category__name': 'office'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == quant

    def test_filter_by_incorrect_category_oddice_admin(self, create_admin, test_password, item_factory, mock_cache):
        """We make sure that we can't find any items even we are admin now"""
        quantity = 7
        item_factory(_quantity=quantity)

        admin = create_admin()
        self.api_client.login(username=admin.username, password=test_password)

        response = self.api_client.get(self.url_list, data={'category__name': 'oddice'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    def teardown(self):

        cache.clear()
