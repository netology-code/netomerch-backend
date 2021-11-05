from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *
from .permissions import *


class BaseViewSet:
    """только админ может удалять, обновлять, создавать, просматривать могут все"""
    # def get_permissions(self):
    #     """Получение прав для действий"""
    #
    #     # TODO: здесь показывает предупреждение, но всё ок, но наследование ModelViewSet нельзя сюда в класс добавить
    #     if self.action in ['create', 'destroy', 'update', 'partial_update']:
    #         return [IsAdmin()]
    #     return []
    pass


class CategoryViewSet(BaseViewSet, ModelViewSet):
    """энд-поинт вью Категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrSafeMethods, ]  # TODO: какой способ лучше? Так, или через функцию?


class ProductViewSet(BaseViewSet, ModelViewSet):
    """энд-поинт вью Продуктов"""
    queryset = Items.objects.all().select_related('category_id')  # TODO: ну вроде ведь надо...
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminOrSafeMethods, ]
