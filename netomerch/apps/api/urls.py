from rest_framework.routers import DefaultRouter

from apps.api.catalog.views import CatalogViewSet

router = DefaultRouter()
router.register("catalog", CatalogViewSet, basename="catalog")

urlpatterns = router.urls
