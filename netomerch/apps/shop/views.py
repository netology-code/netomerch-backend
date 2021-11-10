# from rest_framework.viewsets import ModelViewSet
#
# from .serializers import *
# from .models import *
# from .permissions import *
#
#
# class BaseViewSet:
#     """только админ может удалять, обновлять, создавать, просматривать могут все"""
#     def get_permissions(self):
#         """Получение прав для действий"""
#
#         # TODO: здесь показывает предупреждение, но всё ок, но наследование ModelViewSet нельзя сюда в класс добавить
#         if self.action in ['create', 'destroy', 'update', 'partial_update']:
#             return [IsAdmin()]
#         return []
#     pass
# #
# #
# class CategoryViewSet(BaseViewSet, ModelViewSet):
#     pass
# #
# #
# class ProductViewSet(BaseViewSet, ModelViewSet):
#     pass
