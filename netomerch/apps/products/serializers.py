from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.products.models import Category, Image, Item
from apps.reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'short_description', 'description', 'image')


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'image')


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    properties = serializers.JSONField()

    category = CategorySerializer(many=True, read_only=True)
    tags = TagListSerializerField()
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ("id", "name", "short_description", "description", "image", "tags", "category", "properties")


class ItemMainPageSerializer(serializers.ModelSerializer):
    """сериализатор товара для главной страницы api/v1/main/"""
    item_id = serializers.IntegerField(source="id")
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ("item_id", "name", "image")


class ReviewMainPageSerializer(serializers.ModelSerializer):
    """сериализатор отзывов для главной страницы"""
    item = ItemMainPageSerializer()

    class Meta:
        model = Review
        fields = ("id", "text", "author", "item")


class MainPageSerializer(serializers.Serializer):
    """сериализатор для главной страницы - отзывы + популярные (is_hit) товары"""
    items = ItemMainPageSerializer(many=True)
    reviews = ReviewMainPageSerializer(many=True)
