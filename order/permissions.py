from rest_framework import permissions
from account.enums import UserRoles


class IsNotClient(permissions.IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.role is not UserRoles.client.value


class IsClient(permissions.IsAuthenticated):
    """
    Allows access only to authenticated users.
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id and request.user.role == UserRoles.client.value

    def has_permission(self, request, view):
        return request.user.role is UserRoles.client.value