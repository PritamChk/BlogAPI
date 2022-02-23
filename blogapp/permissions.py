from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Blogger, Blog


class BloggerEditPermission(BasePermission):

    def has_object_permission(self, request, view, obj: Blogger):
        if request.method in SAFE_METHODS:
            return False
        return obj == request.user and request.user.is_authenticated


class BlogEditPermission(BasePermission):

    def has_object_permission(self, request, view, obj: Blog):
        if request.method in SAFE_METHODS:
            return True
        return obj.creator == request.user


class BlogPostPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.creator == request.user and request.user.id == view.kwargs['blogger_pk']


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj

class NotSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user != obj