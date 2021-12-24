from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.catalog.serializers import CatalogSerializer
from apps.products.models import Category, Item, Size, Specialization


class CatalogViewSet(GenericViewSet):
    """контракт каталога api/v1/catalog"""

    def list(self, request):
        serializer = CatalogSerializer(dict(
            categories=Category.objects.all(),
            specialization=Specialization.objects.all(),
            sizes=Size.objects.all(),
            items=Item.objects.filter(is_published=True).
            select_related("category").  # оставляю так, чтобы удобно было комментить 1 строку и смотреть на запросы
            select_related("specialization").
            prefetch_related("size").
            prefetch_related("onitem").
            all(),
        ),
            context=self.get_serializer_context()
        )
        return Response(serializer.data)
