from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.products.models import Category, ItemJSON


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('name', 'id')


class ItemJSONSerializer(TaggitSerializer, serializers.ModelSerializer):
    property = serializers.JSONField()

    category = CategorySerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = ItemJSON
        fields = ("id", "item_name", "short_description", "description", "image", "tags", "category", "property")
