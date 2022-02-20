from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .models import Blogger, Blog, Comment
from .serializer import *


class BloggerViewSet(ModelViewSet):
    http_methods = ["get", "post", 
                    # "patch", #FIXME : HERE 
                    "delete", "head", "option"]
    queryset = Blogger.objects.all()
    
    def get_queryset(self):
        # FIXME : PATCH
        # if self.request.method == "PATCH":
        #     return Blogger.objects.filter(self.kwargs['pk']).first()
        return Blogger.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerCreateSerializer
        #FIXME : PATCH
        # elif method == "PATCH":
        #     return BloggerPatchSerializer
        return SimpleBloggerSerializer

    #FIXME : Patch no working Properly
    # @action(methods=["patch"],detail=False,url_name='blogger update')
    # def patch(self,request,*args,**kwargs):
    #     pass
