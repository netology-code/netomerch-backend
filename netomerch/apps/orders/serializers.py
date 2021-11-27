from rest_framework import serializers

from apps.orders.models import ItemConnections, Order


class ItemConnectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemConnections
        fields = ('items', 'count')


class OrderSerializer(serializers.ModelSerializer):
    item = ItemConnectionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'total_sum', 'final_sum', 'address', 'item',)

    def create(self, validated_data):
        items = validated_data.pop('item')
        discount = validated_data['total_sum'] - validated_data['final_sum']
        if discount != 0:
            validated_data['discount'] = discount

        order = super().create(validated_data)

        for item in items:
            item = dict(item)
            ItemConnections.objects.create(orders=order, items=item['items'], count=item['count'])
        return order
