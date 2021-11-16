from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.products.models import Category, CategoryJSON, Item, ItemJSON


class CategorySerializer(serializers.ModelSerializer):
    """сериализатор для категорий товаров"""

    class Meta:
        model = Category  # здесь просто указываем модель
        fields = ("id", "category_name", "short_description", "description", "image")  # "__all__"


class ItemSerializer(serializers.ModelSerializer):
    """сериализатор для товаров (продуктов)"""
    category_id = serializers.StringRelatedField()

    class Meta:
        model = Item  # здесь просто указываем модель
        fields = ("id", "item_name", "short_description", "description", "image", "category_id")


class CategoryJSONSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = CategoryJSON
        fields = ('category_name', 'id')


class ItemJSONSerializer(TaggitSerializer, serializers.ModelSerializer):
    properties = serializers.JSONField()

    category = CategoryJSONSerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = ItemJSON
        fields = ("id", "item_name", "short_description", "description", "image", "tags", "category", "properties")
