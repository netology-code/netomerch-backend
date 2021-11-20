from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ItemJSONViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
# router.register('items', ItemViewSet, basename='items')
router.register('itemsjson', ItemJSONViewSet)

urlpatterns = router.urls
