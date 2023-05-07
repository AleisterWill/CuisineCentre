from rest_framework import permissions


class IsStoreOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, cuahang):
        return request.user and request.user == cuahang.user and request.user.is_store_owner
