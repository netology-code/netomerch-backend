from rest_framework import serializers

from apps.products.models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    """сериализатор для категорий товаров"""
    class Meta:
        model = Category  # здесь просто указываем модель
        fields = ("id", "name", "short_description", "description", "image", "count")  # "__all__"


class ItemSerializer(serializers.ModelSerializer):
    """сериализатор для товаров (продуктов)"""
    category_id = serializers.StringRelatedField()

    class Meta:
        model = Item  # здесь просто указываем модель
        fields = ("id", "item_name", "short_description", "description", "image", "category_id")
