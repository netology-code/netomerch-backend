from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ItemViewSet, MainPageViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('items', ItemViewSet, basename='items')
router.register('main', MainPageViewSet, basename='main')

urlpatterns = router.urls
