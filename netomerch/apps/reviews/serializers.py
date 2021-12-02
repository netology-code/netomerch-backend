from rest_framework import serializers

from apps.orders.models import ItemConnections
from apps.reviews.models import Review


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemConnections
        fields = ('items', 'orders')


class ReviewSerializer(serializers.ModelSerializer):
    orders_item = OrderItemSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'email', 'text', 'is_published', 'orders_item')


class SendReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'orders_item')
