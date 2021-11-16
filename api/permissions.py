from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrStaffReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (((request.user.role_is_moderator or request.user.role_is_admin)
                if hasattr(request.user, "role")
                else False)
                or obj.author == request.user
                or request.method in SAFE_METHODS)


class IsAdminOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role_is_admin
                if hasattr(request.user, "role") else False
                or request.method in SAFE_METHODS)


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role_is_admin
                if hasattr(request.user, "role") else False)
