from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.products.models import CategoryJSON, ItemJSON


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
