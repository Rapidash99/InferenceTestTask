from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsSenderOrReceiver(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.receiver


class IsSender(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user


class IsSenderOrReadOnlyReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or (request.user == obj.receiver and request.method in SAFE_METHODS)
