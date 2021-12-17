from rest_framework import serializers

from apps.api.card.serializers import CardSerializer
from apps.orders.models import ItemConnections, Order, Promocode
from apps.products.models import Item


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

        if 'promocode' in validated_data.keys():
            promo = Promocode.objects.filter(pk=validated_data['promocode'].code).first()

            if promo.email != validated_data['email']:
                raise serializers.ValidationError('Указанный email не привязан к данному промокоду')

            elif not promo.is_active:
                raise serializers.ValidationError('Прокод не действителен')

            promo.is_active = False
            promo.save()

        order = super().create(validated_data)

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
