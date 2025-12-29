from __future__ import annotations

from typing import Any

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    """Allow access only to Django superusers (shop owner)."""

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsSuperAdminOrReadOnly(BasePermission):
    """Write permissions only for super admin; read for everyone."""

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsOwnerOrSuperAdmin(BasePermission):
    """Object-level permission: owner or super admin only."""

    def has_object_permission(self, request, view, obj: Any) -> bool:  # type: ignore[override]
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        # Many objects will have a `user` attribute
        owner = getattr(obj, "user", None)
        return owner == user
