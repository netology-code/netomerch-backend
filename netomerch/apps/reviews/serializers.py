from datetime import datetime as dt

from rest_framework import serializers

from apps.orders.models import Order
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    date = serializers.SerializerMethodField(source="dt_created")

    class Meta:
        model = Review
        fields = ('id', 'item_id', 'author', 'email', 'text', 'order_id', 'is_published', 'date')

    def get_date(self, instance):
        return dt.date(instance.dt_created).strftime('%d.%m.%Y')


class SendReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'item', 'author', 'email', 'order', 'text')

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

    def validate(self, attrs):
        attr_order = attrs['order']
        attr_item = attrs['item']
        if Order.objects.filter(id=attr_order.id, item=attr_item.id).all().count() == 0:
            raise serializers.ValidationError('item doesn''t belong to order')
        return super().validate(attrs)
