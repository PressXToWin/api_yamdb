from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Даёт доступ только пользователям с ролью админа
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.role == 'admin' or request.user.is_superuser))
