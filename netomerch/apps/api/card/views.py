from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.products.models import Item

from .serializers import CardSerializer


class cardEndPointView(ViewSet):
    """
    end-point of card /api/v1/card/<int>/
    Everybody can
    Anybody can access to method GET only
    User can see only is_published=True card
    """

    def retrieve(self, request, pk=None):
        queryset = Item.objects.filter(is_published=True).all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = CardSerializer(item, context={"request": request})
        return Response(serializer.data)
