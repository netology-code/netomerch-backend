from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ItemViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('items', ItemViewSet, basename='items')

urlpatterns = router.urls
