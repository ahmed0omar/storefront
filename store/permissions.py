from rest_framework import permissions
class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user and request.user.is_staff)
class AdminOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user and request.user.is_authenticated:
            return True
        return (request.user and request.user.is_staff)
#custom model permisions 
class ViewHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return  request.user.has_perm('store.view_history')