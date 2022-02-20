from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .models import Blogger, Blog, Comment
from .serializer import *


    
    
class BloggerViewSet(ModelViewSet):
    http_method_names = [
        "get", "post", 
        "patch",  
        "delete", "head", "option"]
    queryset = Blogger.objects.all()
    
    def get_queryset(self):
        if self.request.method == "PATCH":
            return Blogger.objects.all()
        return Blogger.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerCreateSerializer
        elif method == "PATCH":
            return BloggerPatchSerializer
        return SimpleBloggerSerializer

