from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Даёт доступ неадмину только к GET/OPTIONS/HEAD."""
    
    message = 'Данный запрос недоступен для вас.'
    def has_permission(self, request, view):
        """Проверка на запросы к объекту
        Для безопасных методов всегда True."""
        return (request.method in permissions.SAFE_METHODS
                or (request.user.role == 'admin'))

