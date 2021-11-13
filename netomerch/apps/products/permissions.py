from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """только админ может добавлять, изменять, удалять, но просматривать могут все"""
    def has_permission(self, request, view):
        return request.user.is_superuser
