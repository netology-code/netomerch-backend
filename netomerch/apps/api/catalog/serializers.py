from rest_framework import serializers

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
    color = serializers.CharField(source="color.color_code")

    class Meta:
        model = ImageColorItem
        fields = ("item", "color", "image", "is_main_image", "is_main_color")


class ItemCatalogSerializer(serializers.ModelSerializer):
    """сериализатор товаров для контракта Каталог"""
    item_id = serializers.IntegerField(source="id")
    popular = serializers.BooleanField(source="is_hit")
    size = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")  # [S,L,M,XL,]
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
            "size",
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        item = super(ItemCatalogSerializer, self).to_representation(instance)  # здесь показывает ошибку, но всё норм
        images = item.pop('onitem')  # вот здесь onitem - это related_name из таблицы ItemImageSolor
        colors = []

        if images:
            for image in images:
                if image["color"] not in colors:
                    colors.append(image["color"])

                if image['is_main_color']:
                    full_url = request.build_absolute_uri(image["image"])
                    item['image'] = full_url
                    # break  # пришлось убрать, ведь по всем теперь надо пройти, чтобы цвета набрать

            item["colors"] = colors

        else:
            item['image'] = None
            item['colors'] = None

        return item


class CatalogSerializer(serializers.Serializer):
    """сериализатор Каталога"""
    categories = CategoryCatalogSerializer(many=True)
    specialization = SpecializationCatalogSerializer(many=True)
    sizes = SizeCatalogSerializer(many=True)
    items = ItemCatalogSerializer(many=True)
