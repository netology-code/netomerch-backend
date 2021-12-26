import uuid

import pytest
from django.core.cache import cache
from model_bakery import baker

from apps.api.orders.views import OrderViewSet


@pytest.fixture
def category_factory():
    """автоматическое создание категорий с учётом модели Категория через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('tests.cat_recipe', **kwargs)
    return factory


@pytest.fixture
def specialization_factory():
    """автоматическое создание специализация с учётом модели специализация через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('tests.spec_recipe', **kwargs)
    return factory


@pytest.fixture
def size_factory():
    """автоматическое создание размеров с учётом модели Размеры через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('tests.size_recipe', **kwargs)
    return factory


@pytest.fixture
def color_factory():
    """автоматическое создание цветов с учётом модели Цвета через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('tests.color_recipe', **kwargs)
    return factory


@pytest.fixture
def item_factory():
    """автоматическое создание списка свойств товара с учётом модели ItemProperty через фабрику"""
    def factory(**kwargs):
        size_sets = baker.prepare_recipe('tests.size_recipe', **kwargs)
        color_sets = baker.prepare_recipe('tests.color_recipe', **kwargs)
        return baker.make_recipe('tests.item_recipe',
                                 size=size_sets,
                                 imagecolor=color_sets,
                                 **kwargs)
    return factory


@pytest.fixture
def promo_factory():
    """автоматическое создание списка свойств товара с учётом модели ItemProperty через фабрику"""
    def factory(**kwargs):
        return baker.make_recipe('tests.promo_recipe', **kwargs)
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
    mocker.patch('apps.api.orders.views.OrderViewSet.create', create)


@pytest.fixture
def mock_get_colors(mocker):

    def get_colors(self, item):
        return ['Null']
    mocker.patch('apps.api.card.serializers.CardSerializer.get_colors', get_colors)
