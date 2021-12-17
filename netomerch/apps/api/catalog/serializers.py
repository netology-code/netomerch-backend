from rest_framework import serializers

from apps.api.get_item_main_image import to_representation
from apps.products.models import Category, ImageColorItem, Item, Size, Specialization


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


class ImageColorItemSerializer(serializers.ModelSerializer):
    """сериализатор для таблицы связей товаров с цветами для контракта Каталог"""
    class Meta:
        model = ImageColorItem
        fields = ("item", "color", "image", "is_main_image", "is_main_color")


class GetFieldName(serializers.RelatedField):
    """для того, чтобы size был [L,S,XL,], а не [1,2,3]"""
    def to_representation(self, field):
        return field.name


class ItemCatalogSerializer(serializers.ModelSerializer):
    """сериализатор товаров для контракта Каталог"""
    item_id = serializers.IntegerField(source="id")
    popular = serializers.BooleanField(source="is_hit")
    sizes = GetFieldName(many=True, read_only=True, source="size")  # names [S,L,M,XL,], а не id [1,2,3]
    specialization = serializers.CharField(source="specialization.name")  # {spec: web}, а не id {spec: 1}
    category = serializers.CharField(source="category.name")  # {category: футболки}, а не id {category: 1}
    onitem = ImageColorItemSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = (
            "item_id",
            "name",
            "popular",
            "short_description",
            "onitem",
            "price",
            "category",
            "specialization",
            "sizes",
        )

    def to_representation(self, instance):
        return to_representation(self, instance, ItemCatalogSerializer)


class CatalogSerializer(serializers.Serializer):
    """сериализатор Каталога"""
    categories = CategoryCatalogSerializer(many=True)
    specialization = SpecializationCatalogSerializer(many=True)
    sizes = SizeCatalogSerializer(many=True)
    items = ItemCatalogSerializer(many=True)
