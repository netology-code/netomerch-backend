from rest_framework import serializers

from apps.products.models import Category, CategoryJSON, Item, ItemJSON

from taggit.serializers import (TagListSerializerField, TaggitSerializer)


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
    # category_name = serializers.CharField(source='categoryjson__category_name')

    class Meta:
        model = CategoryJSON
        fields = ('category_name', )


# class CategoryJSONSerializer(serializers.ModelSerializer):
#     category = CategoryJSONSerializer(many=True, read_only=True)

#     class Meta:
#         model = ItemJSON
#         fields = ('category', )


class ItemJSONSerializer(TaggitSerializer, serializers.ModelSerializer):
    # category = serializers.ListField()
    # properties = serializers.JSONField()

    category = CategoryJSONSerializer(many=True, read_only=True)
    # print(f"\n\n\n\n\n\n category:  {category} \n\n\n\n\n\n\n")
    tags = TagListSerializerField()

    class Meta:
        model = ItemJSON
        fields = ("id", "item_name", "short_description", "description", "image", "tags", "category")
