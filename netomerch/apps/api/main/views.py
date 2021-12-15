from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.api.main.serializers import MainPageSerializer
from apps.products.models import Item
from apps.reviews.models import Review


class MainPageViewSet(ViewSet):

    @staticmethod
    def list(request):
        serializer = MainPageSerializer(dict(

            reviews=Review.objects.filter(is_published=True).
            select_related("item").
            prefetch_related("item__onitem").
            all(),

            popular=Item.objects.filter(is_hit=True).
            prefetch_related("onitem").
            all(),

        ),
            context={"request": request}
        )
        return Response(serializer.data)
