from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from termcolor import colored

from .filters import BloggerFilter
from .models import Blog, Blogger, Comment
from .serializers import *


class BloggerViewSet(ModelViewSet):
    # http_method_names = [
    #     "get", #FIXME : NEED TO BE REMOVED
    #     "head",
    #     "option"
    # ]
    # serializer_class = SimpleBloggerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = BloggerFilter
    search_fields = ["first_name", "last_name", "username", "email"]
    ordering_fields = ["first_name", "last_name", "email"]
    # permission_classes = [IsAuthenticated]
    queryset = Blogger.objects.all()

    def get_permissions(self): #FIXME : NOT WORKING LIKE MOSH : lec : 11
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerCreateSerializer
        elif method == "PATCH":
            return BloggerPatchSerializer
        return SimpleBloggerSerializer  # FIXME : NEED TO BE REMOVED

    @action(detail=False, methods=["GET", "PUT"])  # FIXME
    def me(self, request):
        blogger, created = Blogger.objects.get_or_create(
            id=self.request.user.id)
        if request.method == "GET":
            serializer = SimpleBloggerSerializer(blogger)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = BloggerPatchSerializer(blogger,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class BlogVSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "option", "head"]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        return Blog.objects.select_related('creator')\
            .prefetch_related('comments')\
            .filter(creator__id=self.kwargs.get('blogger_pk'))

    def get_serializer_class(self):
        method = self.request.method
        if method == "PATCH":
            return BlogPatchSerializer
        elif method == "POST":
            return BlogPostSerializer
        return BlogReadSerializer

    def get_serializer_context(self):
        return {"creator_id": self.kwargs['blogger_pk']}


class AllBlogVSet(ListModelMixin, GenericViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "created_at"]
    queryset = Blog.objects.select_related(
        'creator').prefetch_related('comments').all()
    serializer_class = BlogReadSerializer


class CommentVSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "option", "head"]

    def get_queryset(self):
        return Comment.objects.select_related('blog')\
            .select_related('commentor')\
            .filter(
                commentor__id=self.kwargs.get('blogger_pk'),
                blog__id=self.kwargs.get('blogs_pk')
        )

    def get_serializer_context(self):
        return {
            'blogger_pk': self.kwargs['blogger_pk'],
            'blog_pk': self.kwargs['blogs_pk']
        }

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return CommentsPostSerializer
        elif method == "PATCH":
            return CommentsPatchSerializer
        return CommentsGetSerializer
