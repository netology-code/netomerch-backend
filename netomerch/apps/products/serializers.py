from rest_framework import serializers

from apps.products.models import Category, Item, ItemJSON


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


class ItemJSONSerializer(serializers.ModelSerializer):
    # category = serializers.ListField()
    # properties = serializers.JSONField()
    # tags = serializers.ListField()

    class Meta:
        model = ItemJSON
        fields = ("id", "item_name", "short_description", "description", "image")
