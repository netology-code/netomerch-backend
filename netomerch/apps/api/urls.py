from rest_framework.routers import DefaultRouter

from apps.api.catalog.views import CatalogViewSet
from apps.api.main.views import MainPageViewSet

router = DefaultRouter()
router.register("catalog", CatalogViewSet, basename="catalog")
router.register("main", MainPageViewSet, basename="main")

urlpatterns = router.urls
