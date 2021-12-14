import uuid

import pytest
from django.core.cache import cache
from model_bakery import baker

from apps.api.orders.views import OrderViewSet


@pytest.fixture
def category_factory():
    """автоматическое создание категорий с учётом модели Категория через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('apps.products.cat_recipe', **kwargs)
    return factory


@pytest.fixture
def itemproperty_factory():
    """автоматическое создание списка свойств товара с учётом модели ItemProperty через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('apps.products.prop_recipe', **kwargs)
    return factory


@pytest.fixture
def item_factory():
    """автоматическое создание списка свойств товара с учётом модели ItemProperty через фабрику"""
    def factory(**kwargs):
        cat_sets = baker.prepare_recipe('apps.products.cat_recipe', **kwargs)
        return baker.make_recipe('apps.products.item_recipe', category=cat_sets, **kwargs)
    return factory


@pytest.fixture
def test_password():
    return 'VEry-1-strong-test-passWorD'


@pytest.fixture
def create_admin(db, django_user_model, test_password):
    def make_admin(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        admin_user = django_user_model.objects.create_superuser(is_staff=True, is_superuser=True, **kwargs)
        return admin_user
    return make_admin


@pytest.fixture
def create_customer(db, django_user_model, test_password):
    def make_customer(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        customer = django_user_model.objects.create_user(is_staff=False, is_superuser=False, **kwargs)
        return customer
    return make_customer


@pytest.fixture
def mock_cache(mocker):
    """Заменяем функцию process_response, чтобы не было записи в кеш"""

    def mocks(self, request, response):
        return response
    mocker.patch('django.middleware.cache.CacheMiddleware.process_response', mocks)


@pytest.fixture
def mock_cache_set(mocker):
    """Устанавливаем понятный ключ для кеша, который можно вытащить в тестах."""

    def set_cache(self, request, response):
        cache.set(request.get_full_path(), response)
        return response
    mocker.patch('django.middleware.cache.CacheMiddleware.process_response', set_cache)


@pytest.fixture
def mock_sendmail(mocker):

    def create(self, request, *args, **kwargs):
        return super(OrderViewSet, self).create(request, *args, **kwargs)
    mocker.patch('apps.orders.views.OrderViewSet.create', create)
