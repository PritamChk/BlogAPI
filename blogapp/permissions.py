from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Blogger, Blog


class BloggerEditPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj: Blogger):
        if request.method in SAFE_METHODS:
            return False
        return obj == request.user


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
    # def has_permission(self, request, view):
    #     if request.method in SAFE_METHODS:
    #         return True
    #     return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class NotSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user != obj


class BlogPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.blogs


class IsBlogOwner(BasePermission):
    message = "You are not the owner of this Blog"
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user

class IsOwnerOfComment(BasePermission):
    message = "You are not the owner of this comment"
    def has_object_permission(self, request, view, obj):
        return bool(obj.commentor==request.user)