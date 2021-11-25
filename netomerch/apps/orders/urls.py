from rest_framework.routers import DefaultRouter

from apps.orders.views import OrderViewSet
from config import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = router.urls
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
