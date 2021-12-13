from rest_framework import serializers

from apps.orders.models import ItemConnections, Order, Promocode


class ItemConnectionsSerializer(serializers.ModelSerializer):
    item_id = serializers.CharField(source='item')

    class Meta:
        model = ItemConnections
        fields = ('item_id', 'count', 'size', 'color', 'price', 'image')

class OrderSerializer(serializers.ModelSerializer):
    items = ItemConnectionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'address', 'items', 'comment', 'total_sum', 'final_sum', 'promocode')

    def create(self, validated_data):
        items = validated_data.pop('items')
        print(validated_data)
        print(items)

        order = super().create(validated_data)

        for item in items:
            item = dict(item)
            print(item)
            ItemConnections.objects.create(order=order, item_id=item['item'], count=item['count'], price=item['price'],
                                           color=item['color'], size=item['size'], image=item['image'])

        print('Create ok')
        return order
