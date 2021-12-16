from rest_framework import serializers
from apps.orders.models import ItemConnections, Order, Promocode
from apps.products.models import Item
from apps.api.card.serializers import CardSerializer


class ItemConnectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemConnections
        fields = ('item', 'count', 'size', 'color', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = ItemConnectionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'address', 'comment', 'total_sum', 'final_sum', 'promocode', 'items')

    def create(self, validated_data):
        items = validated_data.pop('items')

        order = super().create(validated_data)
        Promocode.objects.filter(pk=validated_data['promocode'].code).update(is_active=False)


        for item in items:
            item = dict(item)
            ItemConnections.objects.create(order=order, item=item['item'], count=item['count'], price=item['price'],
                                           color=item['color'], size=item['size'])

        return order


class PromoCardSerializer(CardSerializer):
    class Meta:
        model = Item
        fields = ("item_id", "name", "description", "price", "colors", "sizes",)


class PromocodeSerializer(serializers.ModelSerializer):

    item = PromoCardSerializer()

    class Meta:
        model = Promocode
        fields = ('code', 'item')
