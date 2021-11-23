import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from apps.products.models import ItemProperty


@pytest.mark.django_db
class TestItemPropertyBaker:
    """Let's test API of item's properties"""

    def setup(self):
        """This method is run every time when we run another test"""
        self.url_list = reverse('itemproperties-list')

        # Do we have an empty database?
        self.api_client = APIClient()
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    @staticmethod
    def create_instances():
        """This method provides the ability to reuse code"""
        ItemProperty.objects.create(name='size', type='TEXT', description='Размер товара')
        ItemProperty.objects.create(name='color', type='TEXT', description='Цвет товара')
        ItemProperty.objects.create(name='has_print', type='BOOL', description='Наличие принта')
        ItemProperty.objects.create(name='print', type='TEXT', description='Принты')
        ItemProperty.objects.create(name='material', type='TEXT', description='Материал')

    def test_get_all(self, itemproperty_factory, mock_cache):
        """It generates the "quantity" of objects, then we take all of them with the GET method"""

        quantity = 5
        itemproperty_factory(_quantity=quantity)
        response = self.api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        # here we make sure that there are exactly "quantity" of them
        assert len(response.data.get('results')) == quantity

    def test_get_first(self, itemproperty_factory, mock_cache):
        """It generates the "quantity" of objects, then we take the first one with the GET method"""

        quantity = 5
        itemproperty_factory(_quantity=quantity)
        c_1 = ItemProperty.objects.first()
        url = reverse('itemproperties-detail', kwargs={'pk': c_1.pk})
        response = self.api_client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('name') == c_1.name  # names are equal

    def test_without_ordering(self, mock_cache):
        """It generates objects, then we take all of them with the GET method
        In this test we use the "ordering" clause with ordering by pk (created)"""

        self.create_instances()
        response = self.api_client.get(self.url_list, data={'ordering': 'id'})
        first = response.data.get('results')[0]  # the first one
        last = response.data.get('results')[-1]  # the last one
        assert response.status_code == HTTP_200_OK
        # here we make sure that the first's object name is the first's created name,
        #  and that the last's object name is the last's created name
        assert first.get('name') == 'size'
        assert last.get('name') == 'material'

    def test_with_ordering_by_name(self, mock_cache):
        """It generates objects, then we take all of them with the GET method
        In this test we use the "ordering" clause (field 'name')"""

        self.create_instances()
        response = self.api_client.get(self.url_list, data={'ordering': 'name'})
        first = response.data.get('results')[0]
        last = response.data.get('results')[-1]

        assert response.status_code == HTTP_200_OK
        # here we make sure that the first's object name is the first's one sorted by field 'name',
        #  and that the last's object name is the last's one sorted by field 'name'
        assert first.get('name') == 'color'
        assert last.get('name') == 'size'

    def test_count_2_objects_by_search(self, mock_cache):
        """It generates objects, then we make sure that using search string 'PrInT' we can
        find only 2 objects"""

        self.create_instances()
        response = self.api_client.get(self.url_list, data={'search': 'PrInT'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 2

    def test_count_1_object_by_search(self, mock_cache):
        """It generates objects, then we make sure that using search string 'ize' we can
        find only 1 object"""

        self.create_instances()
        response = self.api_client.get(self.url_list, data={'search': 'ize'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 1

    def test_count_0_object_by_search(self, mock_cache):
        """It generates objects, then we make sure that we can't find any
        objects with the search string 'test' """

        self.create_instances()
        response = self.api_client.get(self.url_list, data={'search': 'test'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data.get('results')) == 0

    def teardown(self):
        cache.clear()
