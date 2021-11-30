from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ItemViewSet, ReviewViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('items', ItemViewSet, basename='items')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = router.urls
