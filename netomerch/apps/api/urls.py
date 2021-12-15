from rest_framework.routers import DefaultRouter

from apps.api.card.views import cardEndPointView

router = DefaultRouter()
router.register('card', cardEndPointView, basename='card')

urlpatterns = router.urls
