from datetime import datetime

from rest_framework import serializers

from apps.api.get_item_main_image import to_representation
from apps.products.models import ImageColorItem, Item, Specialization
from apps.reviews.models import Review
from django.conf import settings


class ImageColorItemSerializer(serializers.ModelSerializer):
    """сериализатор для таблицы связей товаров с цветами для контракта Main"""
    class Meta:
        model = ImageColorItem
        fields = ("item", "color", "image", "is_main_image", "is_main_color")


class ItemMainPageSerializer(serializers.ModelSerializer):
    """сериализатор товара для главной страницы api/v1/main/"""
    item_id = serializers.IntegerField(source="id")
    onitem = ImageColorItemSerializer(many=True, read_only=True)  # это related_name из таблицы ImageColorItem

    class Meta:
        model = Item
        fields = ("item_id", "name", "onitem")

    def to_representation(self, instance):
        return to_representation(self, instance, ItemMainPageSerializer)


class ReviewMainPageSerializer(serializers.ModelSerializer):
    """сериализатор отзывов для главной страницы"""
    name = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField(source="dt_created")
    author_image = serializers.SerializerMethodField()

    def _get_path(self, file):
        request = self.context.get('request')
        return str(request.build_absolute_uri("/")) + str(settings.MEDIA_URL)[1:] + file

    class Meta:
        model = Review
        fields = ("id", "text", "author", "author_image", "date", "item_id", "name", "image", )

    def get_date(self, instance):
        return datetime.date(instance.dt_created).strftime("%d.%m.%Y")

    def get_name(self, instance):
        name = Item.objects.filter(id=instance.item_id).values().first()['name']
        return name

    def get_author_image(self, instance):
        speciaization_image = Specialization.objects.filter(
            id=Item.objects.filter(id=instance.item.id).values('specialization').get()["specialization"]) \
            .values().first()
        author_image = speciaization_image['image']
        return self._get_path(author_image)


class MainPageSerializer(serializers.Serializer):
    """сериализатор для главной страницы - отзывы + популярные (is_hit) товары"""
    popular = ItemMainPageSerializer(many=True)
    reviews = ReviewMainPageSerializer(many=True)
