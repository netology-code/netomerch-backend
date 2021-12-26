from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from apps.orders.models import ItemConnections, Order, Promocode
from apps.products.models import Item


class ItemConnectionsSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), source='item')

    class Meta:
        model = ItemConnections
        fields = ('item_id', 'count', 'size', 'color', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = ItemConnectionsSerializer(many=True)
    phone = PhoneNumberField()

    class Meta:
        model = Order
        fields = ('id', 'name', 'email', 'phone', 'address', 'comment', 'total_sum', 'final_sum', 'promocode', 'items')

    def create(self, validated_data):
        items = validated_data.pop('items')

        if 'promocode' in validated_data:
            Promocode.objects.filter(code=validated_data['promocode'].code).update(is_active=False)

        order = super().create(validated_data)

        for item in items:
            item = dict(item)
            ItemConnections.objects.create(order=order, item=item['item'], count=item['count'], price=item['price'],
                                           color=item['color'], size=item['size'])

        return order
