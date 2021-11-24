from rest_framework import serializers

from apps.orders.models import Order
from apps.products.serializers import ItemSerializer


class OrderSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'items')
