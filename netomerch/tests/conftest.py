import uuid

import pytest
from django.core.cache import cache
from model_bakery import baker


@pytest.fixture
def category_factory():
    """автоматическое создание категорий с учётом модели Категория через фабрику"""
    def factory(**kwargs):
        return baker.make('Category', **kwargs)
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
def mock_cache(mocker):
    def mocks(self, request, response):
        return response
    mocker.patch('django.middleware.cache.CacheMiddleware.process_response', mocks)


@pytest.fixture
def mock_cache_set(mocker):
    def set_cache(self, request, response):
        cache.set(request.get_full_path(), response)
        return response
    mocker.patch('django.middleware.cache.CacheMiddleware.process_response', set_cache)
