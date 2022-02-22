from termcolor import colored,COLORS
from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Blogger,Blog


class BloggerEditPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return False
        return request.user and request.user.is_authenticated
        
    
    def has_object_permission(self, request, view, obj: Blogger):
        if request.method in SAFE_METHODS:
            return False
        return obj==request.user and request.user.is_authenticated

class BlogEditPermission(BasePermission):
    def has_object_permission(self, request, view,obj:Blog):
        if request.method in SAFE_METHODS:
            return False
        return bool(obj.creator == request.user and request.user.is_authenticated)