from rest_framework import serializers

from apps.orders.models import Order, ItemConnections
from apps.products.serializers import ItemSerializer




class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'promo', 'items')
