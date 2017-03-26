"""Permissions for api."""
from rest_framework import permissions


class Owner(permissions.BasePermission):
    """Permission to only allow owners of object to view."""

    def has_object_permission(self, request, view, obj):
        """Check object permissions against the request's user."""
        return obj.user == request.user
