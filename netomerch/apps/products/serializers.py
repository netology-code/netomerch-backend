from django.db.models import Prefetch
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField
from django.conf import settings

from apps.products.models import Category, Image, Item
from apps.reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'short_description', 'description', 'image')


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


# def get_image(self, item):
#     request = self.context.get('request')
#     item_first_image = Item.objects.filter(id=item.id).\
#         prefetch_related("image__items__image").\
#         values_list("image__image", flat=True).first()
#     if item_first_image:
#         item_first_image = f'{settings.MEDIA_URL}{item_first_image}'
#         return request.build_absolute_uri(item_first_image)


class ItemMainPageSerializer(serializers.ModelSerializer):
    """сериализатор товара для главной страницы api/v1/main/"""
    item_id = serializers.IntegerField(source="id")
    # image = serializers.SerializerMethodField()
    image = ImageSerializer(many=True, read_only=True)
    # first_image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ("item_id", "name", "image", )

    # def get_image(self, item):
    #     return get_image(self, item)

    def get_first_image(self, obj):
        # if obj.image.first():
        #     print(obj.image.first().image)
        # else:
        #     print(None)
        return "sss"

class ReviewMainPageSerializer(serializers.ModelSerializer):
    """сериализатор отзывов для главной страницы"""
    item_id = serializers.IntegerField(source="item.id")
    # image = serializers.SerializerMethodField()
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ("id", "image", "text", "author", "item_id")

    # def get_image(self, item):
    #     return get_image(self, item)


class MainPageSerializer(serializers.Serializer):
    """сериализатор для главной страницы - отзывы + популярные (is_hit) товары"""
    items = ItemMainPageSerializer(many=True)
    reviews = ReviewMainPageSerializer(many=True)
