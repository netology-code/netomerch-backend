from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.api.catalog.serializers import CatalogSerializer
from apps.products.models import Category, Item, Size, Specialization


class CatalogViewSet(ViewSet):
    """контракт каталога"""

    @staticmethod
    def list(request):
        serializer = CatalogSerializer(dict(
            categories=Category.objects.all(),
            specialization=Specialization.objects.all(),
            sizes=Size.objects.all(),
            items=Item.objects.filter(is_published=True).
            select_related("category").
            select_related("specialization").
            prefetch_related("size").
            prefetch_related("onitem").
            all(),
        ),
            context={"request": request}
        )
        return Response(serializer.data)
