from rest_framework import serializers

from apps.api.get_item_main_image import to_representation
from apps.products.models import ImageColorItem, Item
from apps.reviews.models import Review


class ImageColorItemSerializer(serializers.ModelSerializer):
    """сериализатор для таблицы связей товаров с цветами для контракта Main"""
    class Meta:
        model = ImageColorItem
        fields = ("item", "color", "image", "is_main_image", "is_main_color")


class ItemMainPageSerializer(serializers.ModelSerializer):
    """сериализатор товара для главной страницы api/v1/main/"""
    item_id = serializers.IntegerField(source="id")
    onitem = ImageColorItemSerializer(many=True, read_only=True)  # это related_name из таблицы ImageColorItem

    class Meta:
        model = Item
        fields = ("item_id", "name", "onitem")

    def to_representation(self, instance):
        return to_representation(self, instance, ItemMainPageSerializer)


class ReviewMainPageSerializer(serializers.ModelSerializer):
    """сериализатор отзывов для главной страницы"""
    item = ItemMainPageSerializer()

    class Meta:
        model = Review
        fields = ("id", "text", "author", "item_id", "item")

    def to_representation(self, instance):
        item = super(ReviewMainPageSerializer, self).to_representation(instance)
        images = item.pop("item")
        item['image'] = images.pop('image')
        return item


class MainPageSerializer(serializers.Serializer):
    """сериализатор для главной страницы - отзывы + популярные (is_hit) товары"""
    popular = ItemMainPageSerializer(many=True)
    reviews = ReviewMainPageSerializer(many=True)
