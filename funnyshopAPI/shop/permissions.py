from rest_framework.permissions import BasePermission, SAFE_METHODS

class UserPoermission(BasePermission):
    def has_permission(self, request, view):

        if (view.basename in ["order"]) and request.method in ['GET']:
            return request.user.is_superuser 

        if (view.basename in ["order"]) and request.method in ['POST']:
            return True

        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if request.user.is_superuser:
            return True

        return False


    def has_object_permission(self, request, view, obj):

        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if request.user.is_superuser:
            return True

        return False


