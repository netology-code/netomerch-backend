from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.products.models import Category, ItemJSON, ItemProperty


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'short_description', 'description', 'image')


class ItemPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemProperty
        fields = ('id', 'name', 'type', 'description')


class ItemJSONSerializer(TaggitSerializer, serializers.ModelSerializer):
    property = serializers.JSONField()

    category = CategorySerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = ItemJSON
        fields = ("id", "item_name", "short_description", "description", "image", "tags", "category", "property")
