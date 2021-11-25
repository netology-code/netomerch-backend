from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def create(self, request, *args, **kwargs):
    #     order = super().create(self, request, *args, **kwargs)
