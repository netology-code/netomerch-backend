from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.api.main.serializers import MainPageSerializer
from apps.products.models import Item
from apps.reviews.models import Review


class MainPageViewSet(ViewSet):

    @staticmethod
    def list(request):
        serializer = MainPageSerializer(dict(
            reviews=Review.objects.filter(is_published=True).all().select_related("item"),
            popular=Item.objects.filter(is_hit=True).all()),
            context={"request": request}
        )
        return Response(serializer.data)
