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

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Item.objects.all()
        else:
            queryset = Item.objects.filter(is_published=True).all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        print(request.query_params)
        print(kwargs)

        pk = kwargs['pk']
        queryset = self.get_queryset()
        queryset = queryset.filter(pk=pk).all()
        # item = get_object_or_404(queryset, pk=pk)

        # ,            item=Review.objects.filter(is_published=True).all().select_related("item"),
        serializer_class = cardSerializer(dict(item=queryset), context={"request": request})
        return Response(serializer_class.data)
