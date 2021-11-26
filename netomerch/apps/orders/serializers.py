from rest_framework import serializers

from apps.orders.models import ItemConnections, Order
from apps.products.models import Item


class ItemConnectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemConnections
        fields = ('items', 'count')


class OrderSerializer(serializers.ModelSerializer):
    item = ItemConnectionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'promo', 'item')

    def create(self, validated_data):
        items = validated_data.pop('item')
        order = super().create(validated_data)

        for item in items:
            item = dict(item)
            ItemConnections.objects.create(orders=order, items=item['items'], count=item['count'])
        return order
