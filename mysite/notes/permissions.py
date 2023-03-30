from rest_framework import permissions
from django.contrib.auth.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class DoesntDone(IsAdminOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and not obj.is_done
