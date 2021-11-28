from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from apps.products.models import Category, Item, ItemProperty
from apps.products.permissions import IsAdmin
from apps.products.serializers import CategorySerializer, ItemPropertySerializer, ItemSerializer


class BaseViewSet:
    """только админ может удалять, обновлять, создавать, а просматривать могут все"""

    def get_permissions(self):
        """Получение прав для действий"""

        # FIXME: здесь показывает предупреждение, но всё ок. Наследование ModelViewSet нельзя сюда в класс добавить
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAdmin()]
        return []


@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='retrieve')
class CategoryViewSet(BaseViewSet, ModelViewSet):
    """
    Энд-поинт категорий товаров - /api/v1/categories/
    Доступные методы
    - GET - доступно всем
    - POST, PATCH, DELETE - только Админу, остальным 403 запрещено
    """
    queryset = Category.objects.order_by('pk').all()

    serializer_class = CategorySerializer

    search_fields = ['name', 'id']  # поля, по которым доступен поиск ?search=что-то


class ItemPropertyViewSet(BaseViewSet, ModelViewSet):
    """
    Энд-поинт свойств товаров - /api/v1/itemproperties/
    Доступные методы
    - GET - доступно всем
    - POST, PATCH, DELETE - только Админу, остальным 403 запрещено
    """
    queryset = ItemProperty.objects.order_by('name').all()

    serializer_class = ItemPropertySerializer

    search_fields = ['name', 'id']  # поля, по которым доступен поиск ?search=что-то


@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='retrieve')
class ItemViewSet(BaseViewSet, ModelViewSet):
    """
    Энд-поинт товаров (продуктов) - /api/v1/items/
    Доступные методы
    - GET - доступно всем, админы видят все товары, остальные только те, которые is_published
    - POST, PATCH, DELETE - только Админу, остальным 403 запрещено
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    search_fields = ['name']  # поля, по которым доступен поиск ?search=что-то
    filterset_fields = ('category__name', )

    def get_queryset(self):
        """переопределяем кверисет: админ (видит все товары) или не-админ (видят только опубликованные)"""
        if self.request.user.is_superuser:
            queryset = Item.objects.order_by('pk').all().prefetch_related('category')
        else:
            queryset = Item.objects.filter(is_published=True).order_by('pk').all().prefetch_related('category')
        return queryset
