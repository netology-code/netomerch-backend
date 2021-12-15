from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.products.models import Item

from .serializers import cardSerializer


class cardEndPointView(mixins.RetrieveModelMixin, GenericViewSet):
    """
    end-point of card /api/v1/card/<int>/
    Everybody can
    Anybody can access to method GET only
    User can see only is_published=True card
    """

    def get_queryset(self, pk):
        if self.request.user.is_superuser:
            queryset = Item.objects.filter(pk=pk).prefetch_related("onitem").all()
        else:
            queryset = Item.objects.filter(pk=pk, is_published=True).prefetch_related("onitem").all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        print(kwargs)

        pk = kwargs['pk']
        queryset = self.get_queryset(pk)

        serializer_class = cardSerializer(dict(items=queryset), context={"request": request})
        return Response(serializer_class.data)
