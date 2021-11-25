from rest_framework import serializers

from apps.orders.models import Order, ItemConnections
from apps.products.models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id',)

class ItemConnectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemConnections
        fields = ('items', 'count',)


class OrderSerializer(serializers.ModelSerializer):
    item = ItemConnectionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'promo', 'item')


    def create(self, validated_data):
        print(validated_data)
        items = validated_data.pop('item')
        order = super().create(validated_data)

        for item in items:
            item = dict(item)
            print(item)
            ItemConnections.objects.create(orders=order, items=item['items'], count=item['count'])
        return order
