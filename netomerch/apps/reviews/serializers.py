from datetime import datetime as dt

from rest_framework import serializers

from apps.orders.models import ItemConnections, Order
from apps.reviews.models import Review
from apps.products.models import Item, ImageColorItem


class ReviewSerializer(serializers.ModelSerializer):

    date = serializers.SerializerMethodField(source="dt_created")

    class Meta:
        model = Review
        fields = ('id', 'item_id', 'author', 'email', 'text', 'order_id', 'is_published', 'date', 'image')

    def get_date(self, instance):
        return dt.date(instance.dt_created).strftime('%d.%m.%Y')


class SendReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'item', 'author', 'email', 'order', 'text', 'image')

    def validate_item(self, data):
        if data is None:
            raise serializers.ValidationError('field item couldn''t be empty')

        return data

    def validate_author(self, data):
        if data is None:
            raise serializers.ValidationError('field author couldn''t be empty')

        return data

    def validate_order(self, data):
        if data is None:
            raise serializers.ValidationError('field order couldn''t be empty')
        return data

    def get_image(self, data):
        if data is None:
            fields = self.get_fields()
            item_id = fields.item.id
            data = ImageColorItem.objects.filter(id=item_id, is_main_image=True, is_main_color=True).all()
        return data

    def validate(self, attrs):
        attr_order = attrs['order']
        attr_item = attrs['item']
        # attr_image = attrs['item']
        if Order.objects.filter(id=attr_order.id, item=attr_item.id).all().count() == 0:
            raise serializers.ValidationError(f"item {attr_item.id} doesn't belong to order {attr_order.id}")

        return super().validate(attrs)
