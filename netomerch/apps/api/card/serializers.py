from rest_framework import serializers

from apps.products.models import DictImageColor, ImageColorItem, Item


class cardImagesSerializer(serializers.ModelSerializer):
    is_main = serializers.BooleanField(source="is_main_image")

    class Meta:
        model = ImageColorItem
        fields = ("is_main", "image", )


class cardColorsSerializer(serializers.ModelSerializer):
    is_main = serializers.BooleanField(source="is_main_color")
    color = serializers.BooleanField(source="name")

    class Meta:
        model = DictImageColor
        fields = ("is_main", "color", "name_eng", "color_code", )


class cardSerializer(serializers.ModelSerializer):

    # colors = cardColorsSerializer()
    # item_id = serializers.IntegerField(source="id")

    class Meta:
        model = Item
        fields = ("id", "name", "description", "price", )
        # fields = ("id", "name", "description", "price", "colors", )
