# from rest_framework.permissions import BasePermission, SAFE_METHODS
#
#
# class IsAdminOrSafeMethods(BasePermission):
#     """только админ может добавлять, изменять, удалять, но просматривать их могут все"""
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:  # безопасные методы GET, HEAD, OPTIONS - могут все
#             return True
#         return request.user.is_superuser  # остальные методы POST, PATCH, DELETE - только админы
#
#
# class IsAdmin(BasePermission):
#     """только админ может добавлять, изменять, удалять, но просматривать могут все"""
#     def has_permission(self, request, view):
#         return request.user.is_superuser
