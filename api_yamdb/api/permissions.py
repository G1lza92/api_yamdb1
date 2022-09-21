from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.is_staff
        )
# 100% еще ваши пермишены будут а-ля IsAuthorOrReadOnly
# и что то там с админами и модераторами
