from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from .models import Blogger, Blog, Comment
from .serializer import *
from .filters import BloggerSearchFilter, BlogFilter


class BloggerViewSet(ModelViewSet):
    http_method_names = [
        "get", "post",
        "patch",
        "delete", "head", "option"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = BloggerSearchFilter
    search_fields = ["first_name", "last_name", "username", "email"]
    ordering_fields = ["first_name", "last_name", "email"]
    queryset = Blogger.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == "POST":
            return BloggerCreateSerializer
        elif method == "PATCH":
            return BloggerPatchSerializer
        return SimpleBloggerSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class BlogVSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "option", "head"]
    # queryset = Blog.objects.select_related('creator').all()

    def get_queryset(self):
        return Blog.objects.select_related('creator').filter(creator__id=self.kwargs.get('blogger_pk'))

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
    queryset = Blog.objects.select_related('creator').all()
    serializer_class = BlogReadSerializer

# TODO : Implement CommentViewSet
