from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.products.models import Category, Image, Item, ItemProperty, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'short_description', 'description', 'image')


class ItemPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemProperty
        fields = ('id', 'name', 'type', 'description')


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


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'item_id', 'author', 'email', 'text', 'is_published')


class SendReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'item', 'author', 'email', 'text')

    def validate_item(self, data):
        print(f"\n\n\n\n{data}")
        if data is None:
            raise serializers.ValidationError('field item couldn''t be empty')
        return data
