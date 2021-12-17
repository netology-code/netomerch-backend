# import pytest
# from django.core.cache import cache
# from django.urls import reverse
# from rest_framework.status import HTTP_200_OK
# from rest_framework.test import APIClient
#
# # from apps.products.models import Category
#
#
# @pytest.mark.django_db
# class TestCategoryBaker:
#     """Let's test API of item's categories"""
#
#     def setup(self):
#         """This method is run every time when we run another test"""
#         self.url_list = reverse('categories-list')
#
#         # Do we have an empty database?
#         self.api_client = APIClient()
#         response = self.api_client.get(self.url_list)
#         assert response.status_code == HTTP_200_OK
#         assert len(response.data.get('results')) == 0
#
#     def test_get_all(self, category_factory, mock_cache):
#         """It generates the "quantity" of objects, then we take all of them with the GET method"""
#         # quantity = 5
#         # category_factory(_quantity=quantity)
#         # response = self.api_client.get(self.url_list)
#         assert True
#         # assert response.status_code == HTTP_200_OK
#         # assert len(response.data.get('results')) == quantity
#
#     # def test_get_first(self, category_factory, mock_cache):
#     #     """It generates the "quantity" of objects, then we take the first one with the GET method"""
#     #
#     #     quantity = 5
#     #     category_factory(_quantity=quantity)
#     #     c_1 = Category.objects.first()
#     #     url = reverse('categories-detail', kwargs={'pk': c_1.pk})
#     #     response = self.api_client.get(url)
#     #     assert response.status_code == HTTP_200_OK
#     #     assert response.data.get('name') == c_1.name
#     #
#     # def test_without_ordering(self, category_factory, mock_cache):
#     #     """It generates objects, then we take all of them with the GET method
#     #     In this test we use the "ordering" clause with ordering by pk (created)"""
#     #
#     #     quantity = 4
#     #     category_factory(_quantity=quantity)
#     #     response = self.api_client.get(self.url_list, data={'ordering': 'id'})
#     #     cat_first = response.data.get('results')[0]  # the first one
#     #     cat_last = response.data.get('results')[-1]  # the last one
#     #
#     #     assert response.status_code == HTTP_200_OK
#     #     assert cat_first.get('name') == 'present'
#     #     assert cat_last.get('name') == 'wear'
#     #
#     # def test_with_ordering_by_name(self, category_factory, mock_cache):
#     #     """It generates objects, then we take all of them with the GET method
#     #     In this test we use the "ordering" clause (field 'name')"""
#     #
#     #     quantity = 4
#     #     category_factory(_quantity=quantity)
#     #     response = self.api_client.get(self.url_list, data={'ordering': 'name'})
#     #     cat_first = response.data.get('results')[0]  # the first one
#     #     cat_last = response.data.get('results')[-1]  # the last one
#     #
#     #     assert response.status_code == HTTP_200_OK
#     #     assert cat_first.get('name') == 'office'
#     #     assert cat_last.get('name') == 'wear'
#     #
#     # def test_count_2_objects_by_search(self, category_factory, mock_cache):
#     #     """It generates objects, then we make sure that using search string 'Ar' we can
#     #     find only 2 objects"""
#     #
#     #     quantity = 4
#     #     category_factory(_quantity=quantity)
#     #     response = self.api_client.get(self.url_list, data={'search': 'Ar'})
#     #     assert response.status_code == HTTP_200_OK
#     #     assert len(response.data.get('results')) == 2
#     #
#     # def test_count_1_object_by_search(self, category_factory, mock_cache):
#     #     """It generates objects, then we make sure that using search string 'ff' we can
#     #     find only 1 object"""
#     #
#     #     quantity = 4
#     #     category_factory(_quantity=quantity)
#     #     response = self.api_client.get(self.url_list, data={'search': 'FF'})
#     #     assert response.status_code == HTTP_200_OK
#     #     assert len(response.data.get('results')) == 1
#     #
#     # def test_count_0_object_by_search(self, category_factory, mock_cache):
#     #     """It generates objects, then we make sure that we can't find any
#     #     objects with the search string 'test' """
#     #
#     #     quantity = 4
#     #     category_factory(_quantity=quantity)
#     #     response = self.api_client.get(self.url_list, data={'search': 'test'})
#     #     assert response.status_code == HTTP_200_OK
#     #     assert len(response.data.get('results')) == 0
#
#     def teardown(self):
#         cache.clear()
