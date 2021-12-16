from rest_framework import serializers

from apps.products.models import Category, ImageColorItem, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageColorItem
        fields = ('id', 'image')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "short_description", "description", "category")
