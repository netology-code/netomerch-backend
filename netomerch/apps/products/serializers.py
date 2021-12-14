from django.conf import settings
from rest_framework import serializers

from apps.products.models import Category, ImageColorItem, Item, Size, Specialization
from apps.reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageColorItem
        fields = ('id', 'image')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "short_description", "description", "category")


class ItemMainPageSerializer(serializers.ModelSerializer):
    """сериализатор товара для главной страницы api/v1/main/"""
    item_id = serializers.IntegerField(source="id")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ("item_id", "name", "image")

    def get_image(self, item):
        request = self.context.get('request')
        main_image = ImageColorItem.objects.filter(
            item_id=item.id, is_main_color=True, is_main_image=True).values_list("image", flat=True).first()
        if main_image:
            main_image = f'{settings.MEDIA_URL}{main_image}'
            return request.build_absolute_uri(main_image)


class ReviewMainPageSerializer(serializers.ModelSerializer):
    """сериализатор отзывов для главной страницы"""
    # item = ItemMainPageSerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("id", "text", "author", "image", "item_id")

    def get_image(self, review):
        item = review.item
        request = self.context.get('request')
        main_image = ImageColorItem.objects.filter(
            item_id=item, is_main_color=True, is_main_image=True).values_list("image", flat=True).first()
        if main_image:
            main_image = f'{settings.MEDIA_URL}{main_image}'
            return request.build_absolute_uri(main_image)


class MainPageSerializer(serializers.Serializer):
    """сериализатор для главной страницы - отзывы + популярные (is_hit) товары"""
    popular = ItemMainPageSerializer(many=True)
    reviews = ReviewMainPageSerializer(many=True)


class CategoryCatalogSerializer(serializers.ModelSerializer):
    """сериализатор категорий для контракта Каталог"""

    class Meta:
        model = Category
        fields = ("id", "name")


class SizeCatalogSerializer(serializers.ModelSerializer):
    """сериализатор размеров товаров для контракта Каталог"""

    class Meta:
        model = Size
        fields = ("id", "name")


class SpecializationCatalogSerializer(serializers.ModelSerializer):
    """сериализатор специализаций (направлений обучения) товаров для контракта Каталог"""

    class Meta:
        model = Specialization
        fields = ("id", "name")


class GetFieldName(serializers.RelatedField):
    """для того, чтобы size, spec, category были [L,S,XL,], а не [1,2,3]"""
    def to_representation(self, field):
        return field.name


class ItemCatalogSerializer(serializers.ModelSerializer):
    """сериализатор специализаций (направлений обучения) товаров для контракта Каталог"""
    item_id = serializers.IntegerField(source="id")
    popular = serializers.BooleanField(source="is_hit")
    sizes = GetFieldName(many=True, read_only=True, source="size")  # names [S,L,M,XL,], а не id [1,2,3]
    specialization = GetFieldName(many=True, read_only=True)  # names [програм, маркет, ], а не id [1,2,3]
    category = GetFieldName(many=False, read_only=True)  # {category: футболки}, а не {category: 1}
    image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            "item_id",
            "name",
            "popular",
            "short_description",
            "image",
            "price",
            "category",
            "specialization",
            "sizes",
        )

    def get_image(self, item):
        request = self.context.get('request')
        main_image = ImageColorItem.objects.filter(
            item_id=item, is_main_color=True, is_main_image=True).values_list("image", flat=True).first()
        if main_image:
            main_image = f'{settings.MEDIA_URL}{main_image}'
            return request.build_absolute_uri(main_image)


class CatalogSerializer(serializers.Serializer):
    categories = CategoryCatalogSerializer(many=True)
    specialization = SpecializationCatalogSerializer(many=True)
    sizes = SizeCatalogSerializer(many=True)
    items = ItemCatalogSerializer(many=True)
