from rest_framework.routers import DefaultRouter

from apps.api.orders.views import OrderViewSet, PromocodeViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('promo', PromocodeViewSet, basename='promo')

urlpatterns = router.urls
