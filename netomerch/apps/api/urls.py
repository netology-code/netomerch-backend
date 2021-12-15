from rest_framework.routers import DefaultRouter

from apps.api.card.views import cardEndPointView
from apps.api.catalog.views import CatalogViewSet
from apps.api.main.views import MainPageViewSet

router = DefaultRouter()
router.register('card', cardEndPointView, basename='card')
router.register("catalog", CatalogViewSet, basename="catalog")
router.register("main", MainPageViewSet, basename="main")

urlpatterns = router.urls
