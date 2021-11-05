from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    """сериализатор для продуктов"""

    class Meta:
        model = Items  # здесь просто указываем модель
        fields = "__all__"   # поля - или все, или вида ('поле', 'поле',)


class CategorySerializer(serializers.ModelSerializer):
    """сериализатор для категорий"""

    class Meta:
        model = Category  # здесь просто указываем модель
        fields = "__all__"  # поля - или все, или вида ('поле', 'поле',)
