from rest_framework.routers import DefaultRouter

from apps.api.card.views import cardEndPointView
from apps.api.catalog.views import CatalogViewSet
from apps.api.main.views import MainPageViewSet
from apps.api.orders.views import OrderViewSet, PromocodeViewSet

router = DefaultRouter()
router.register('card', cardEndPointView, basename='card')
router.register('catalog', CatalogViewSet, basename='catalog')
router.register('main', MainPageViewSet, basename='main')
router.register('orders', OrderViewSet, basename='orders')
router.register('promo', PromocodeViewSet, basename='promo')

urlpatterns = router.urls
