from rest_framework.routers import DefaultRouter

from apps.products.views import CatalogViewSet, CategoryViewSet, ItemViewSet, MainPageViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('items', ItemViewSet, basename='items')
router.register('main', MainPageViewSet, basename='main')
router.register('catalog', CatalogViewSet, basename='catalog')

urlpatterns = router.urls
